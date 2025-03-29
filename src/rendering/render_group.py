from typing import TYPE_CHECKING

import numpy as np
import zengl

from src.rendering.render_pipeline import RenderPipeline

if TYPE_CHECKING:
    from src.entities.sprite import Sprite


class RenderGroup:
    def __init__(
        self,
        texture: zengl.Image | None,
        vert_shader_path: str,
        frag_shader_path: str,
        uniform_buffer: zengl.Buffer,
        shader_includes: dict[str, str],
        framebuffers: list[zengl.Image],
    ) -> None:
        self.sprites: list["Sprite"] = []
        self.pipeline = RenderPipeline(
            texture=texture,
            vert_shader_path=vert_shader_path,
            frag_shader_path=frag_shader_path,
            uniform_buffer=uniform_buffer,
            shader_includes=shader_includes,
            framebuffers=framebuffers,
        )
        self.instance_data = np.zeros(
            (1, self.pipeline.instance_stride),
            dtype=np.float32,
        )

    def render(self) -> None:
        if not self.sprites:
            return
        if len(self.sprites) > self.instance_data.shape[0]:
            self.instance_data = np.zeros(
                (len(self.sprites) * 2, self.pipeline.instance_stride),
                dtype=np.float32,
            )
        sprites_data = [sprite.pack() for sprite in self.sprites]
        num_empty_sprites = self.instance_data.shape[0] - len(self.sprites)
        zeros = [
            [0.0 for _ in range(self.pipeline.instance_stride)]
            for _ in range(num_empty_sprites)
        ]
        self.instance_data[:] = sprites_data + zeros
        self.pipeline.render(self.instance_data)
