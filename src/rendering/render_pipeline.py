import re
from typing import TYPE_CHECKING, Iterable

import numpy as np
import zengl

if TYPE_CHECKING:
    from zengl import BufferResource, LayoutBinding, SamplerResource


def load_shader(path: str) -> str:
    with open(path, "r") as file:
        return file.read()


class RenderPipeline:
    def __init__(
        self,
        texture: zengl.Image | None,
        vert_shader_path: str,
        frag_shader_path: str,
        uniform_buffer: zengl.Buffer,
        shader_includes: dict[str, str],
        framebuffers: list[zengl.Image],
    ) -> None:
        self.texture = texture
        self.vert_shader_path = vert_shader_path
        self.frag_shader_path = frag_shader_path
        self.uniform_buffer = uniform_buffer
        self.shader_includes = shader_includes
        self.framebuffers = framebuffers
        self.ctx = zengl.context()
        self.vertices = np.array(
            (
                # x, y, u, v
                *(0, 0, 0, 0),  # top-left
                *(1, 0, 1, 0),  # top-right
                *(0, -1, 0, 1),  # bottom-left
                *(0, -1, 0, 1),  # bottom-left
                *(1, 0, 1, 0),  # top-right
                *(1, -1, 1, 1),  # bottom-right
            ),
            dtype=np.float32,
        )
        self.vertex_layout = ("2f 2f", *(0, 1))
        self.instance_layout = ("4f 1f 1f 1f /i", *(2, 3, 4, 5))
        self.vertex_buffer = self.ctx.buffer(self.vertices)
        self.instance_buffer = self.ctx.buffer(size=1)
        self.instance_stride = sum(
            map(int, re.findall(r"\d+", self.instance_layout[0]))
        )
        self.resources: Iterable["BufferResource | SamplerResource"] = [
            {
                "type": "uniform_buffer",
                "binding": 0,
                "buffer": self.uniform_buffer,
            },
        ]
        self.layout: Iterable["LayoutBinding"] = [{"name": "Common", "binding": 0}]
        if self.texture:
            self.resources.append(
                {
                    "type": "sampler",
                    "binding": 0,
                    "image": self.texture,
                    "min_filter": "linear_mipmap_linear",
                    "mag_filter": "linear",
                }
            )
            self.layout.append({"name": f"Texture0", "binding": 0})
        self.template_pipeline = self.ctx.pipeline(
            includes=self.shader_includes,
            vertex_shader=load_shader(self.vert_shader_path),
            fragment_shader=load_shader(self.frag_shader_path),
            framebuffer=self.framebuffers,
            resources=self.resources,
            layout=self.layout,
            blend={
                "enable": True,
                "src_color": "src_alpha",
                "dst_color": "one_minus_src_alpha",
            },
            vertex_buffers=[
                *zengl.bind(self.vertex_buffer, *self.vertex_layout),
                *zengl.bind(self.instance_buffer, *self.instance_layout),
            ],
            vertex_count=self.vertex_buffer.size
            // zengl.calcsize(" ".join([v for v in self.vertex_layout[0].split()])),
        )
        self.pipeline = self.create_pipeline_from_template(1)

    def create_pipeline_from_template(self, instance_data_size: int) -> zengl.Pipeline:
        self.instance_buffer = self.ctx.buffer(size=instance_data_size)
        return self.ctx.pipeline(
            template=self.template_pipeline,
            vertex_buffers=[
                *zengl.bind(self.vertex_buffer, *self.vertex_layout),
                *zengl.bind(self.instance_buffer, *self.instance_layout),
            ],
        )

    def render(self, instance_data: np.ndarray) -> None:
        if instance_data.nbytes > self.instance_buffer.size:
            self.pipeline = self.create_pipeline_from_template(instance_data.nbytes)
        self.instance_buffer.write(instance_data)
        self.pipeline.instance_count = instance_data.shape[0]
        self.pipeline.render()
