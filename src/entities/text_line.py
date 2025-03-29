from typing import TYPE_CHECKING, Callable

from src.entities.sprite import Sprite

if TYPE_CHECKING:
    from src.rendering.render_group import RenderGroup


class TextLine:
    def __init__(
        self,
        callback: Callable[[], str],
        render_group: "RenderGroup",
        font_size: tuple[int, int],
        font_idx_map: dict[str, int],
        pos: tuple[int, int],
        depth: float,
    ):
        self.callback = callback
        self.render_group = render_group
        self.depth = depth
        self.pos = pos
        self.glyphs: list[Sprite] = []
        self.font_size = font_size
        self.font_idx_map = font_idx_map
        self.visible = True

    def create_glyphs(self, num_glyphs: int) -> None:
        for glyph in self.glyphs:
            glyph.delete()
        self.glyphs = [
            Sprite(
                render_group=self.render_group,
                pos=(
                    (i * self.font_size[0] + self.pos[0]),
                    self.pos[1],
                ),
                size=self.font_size,
                depth=self.depth,
            )
            for i in range(num_glyphs + 1)
        ]

    def update(self) -> None:
        text = self.callback() if self.visible else ""
        if len(text) > len(self.glyphs):
            self.create_glyphs(len(text))

        for i, glyph in enumerate(text):
            glyph_sprite = self.glyphs[i]
            glyph_sprite.tex_idx = self.font_idx_map[glyph]

        num_glyphs = len(self.glyphs)
        if len(text) < num_glyphs:
            for i in range(len(text), num_glyphs):
                self.glyphs[i].tex_idx = self.font_idx_map[" "]
