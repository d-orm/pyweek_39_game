import struct
from collections import deque
from typing import TYPE_CHECKING

import zengl

if TYPE_CHECKING:
    from webwindow import WebWindow  # type: ignore

    from src.window.pygame_window import PygameWindow

from src.rendering.render_group import RenderGroup
from src.rendering.textures import Textures


class Renderer:
    def __init__(self, window: "WebWindow | PygameWindow") -> None:
        self.window = window
        self.ctx = zengl.context()
        self.fbo = self.ctx.image(self.window.size, "rgba8unorm")
        self.fbo.clear_value = (0.1, 0.2, 0.5, 1.0)
        self.depth_fbo = self.ctx.image(self.window.size, "depth24plus")
        self.num_entities = 0
        self.fps_q: deque[float] = deque(maxlen=100)
        self.avg_fps = 0.0
        self.shader_constants_string = f"""
            const vec2 iResolution = vec2({float(self.window.size[0])}, {float(self.window.size[1])});
        """
        self.std140_layout_string = """
            layout (std140) uniform Common {
                float iTime;
            };
        """
        self.shader_includes = {
            "uniforms": self.std140_layout_string,
            "constants": self.shader_constants_string,
        }
        self.uniforms_buffer_struct_layout = "1f"
        self.uniforms_buffer_struct_size = struct.calcsize(
            self.uniforms_buffer_struct_layout
        )
        self.uniform_buffer = self.ctx.buffer(
            size=16 + self.uniforms_buffer_struct_size
        )
        self.textures = Textures()
        self.render_groups = {
            "default": RenderGroup(
                texture=self.textures.default_texture,
                vert_shader_path="src/rendering/shaders/default.vert",
                frag_shader_path="src/rendering/shaders/default.frag",
                uniform_buffer=self.uniform_buffer,
                shader_includes=self.shader_includes,
                framebuffers=[self.fbo, self.depth_fbo],
            ),
            "datastream": RenderGroup(
                texture=None,
                vert_shader_path="src/rendering/shaders/default.vert",
                frag_shader_path="src/rendering/shaders/datastream.frag",
                uniform_buffer=self.uniform_buffer,
                shader_includes=self.shader_includes,
                framebuffers=[self.fbo, self.depth_fbo],
            ),
            "circuit_board": RenderGroup(
                texture=self.textures.circuit_board_texture,
                vert_shader_path="src/rendering/shaders/default.vert",
                frag_shader_path="src/rendering/shaders/default.frag",
                uniform_buffer=self.uniform_buffer,
                shader_includes=self.shader_includes,
                framebuffers=[self.fbo, self.depth_fbo],
            ),
            "font": RenderGroup(
                texture=self.textures.font_texture,
                vert_shader_path="src/rendering/shaders/default.vert",
                frag_shader_path="src/rendering/shaders/default.frag",
                uniform_buffer=self.uniform_buffer,
                shader_includes=self.shader_includes,
                framebuffers=[self.fbo, self.depth_fbo],
            ),
            "ui_panel": RenderGroup(
                texture=self.textures.ui_panel_texture,
                vert_shader_path="src/rendering/shaders/default.vert",
                frag_shader_path="src/rendering/shaders/default.frag",
                uniform_buffer=self.uniform_buffer,
                shader_includes=self.shader_includes,
                framebuffers=[self.fbo, self.depth_fbo],
            ),
            "player": RenderGroup(
                texture=self.textures.robot_texture,
                vert_shader_path="src/rendering/shaders/default.vert",
                frag_shader_path="src/rendering/shaders/default.frag",
                uniform_buffer=self.uniform_buffer,
                shader_includes=self.shader_includes,
                framebuffers=[self.fbo, self.depth_fbo],
            ),
            "intro_panel": RenderGroup(
                texture=self.textures.intro_panel_texture,
                vert_shader_path="src/rendering/shaders/default.vert",
                frag_shader_path="src/rendering/shaders/default.frag",
                uniform_buffer=self.uniform_buffer,
                shader_includes=self.shader_includes,
                framebuffers=[self.fbo, self.depth_fbo],
            ),
        }
        for obs_id, obs_texture in self.textures.obstacle_textures.items():
            self.render_groups[obs_id] = RenderGroup(
                texture=obs_texture,
                vert_shader_path="src/rendering/shaders/default.vert",
                frag_shader_path="src/rendering/shaders/default.frag",
                uniform_buffer=self.uniform_buffer,
                shader_includes=self.shader_includes,
                framebuffers=[self.fbo, self.depth_fbo],
            )

    def get_avg_fps(self) -> None:
        ft = self.window.frame_time
        fps = 1 / ft if ft > 0 else 0
        self.fps_q.append(fps)
        self.avg_fps = sum(self.fps_q) / len(self.fps_q)

    def write_uniforms(self) -> None:
        self.uniform_buffer.write(
            struct.pack(self.uniforms_buffer_struct_layout, self.window.time)
        )

    def render(self) -> None:
        self.write_uniforms()
        self.get_avg_fps()
        self.ctx.new_frame()
        self.fbo.clear()
        self.num_entities = 0
        self.depth_fbo.clear()
        for render_group in self.render_groups.values():
            render_group.render()
            # self.num_entities += render_group.instance_data.shape[0]
        self.fbo.blit()
        self.ctx.end_frame()
