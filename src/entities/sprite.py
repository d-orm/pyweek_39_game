import math
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from src.rendering.render_group import RenderGroup


class Sprite:
    def __init__(
        self,
        render_group: "RenderGroup",
        pos: pygame.Vector2 | tuple[float | int, float | int],
        size: pygame.Vector2 | tuple[float | int, float | int],
        rot: float = 0.0,
        tex_idx: float = 0.0,
        depth: float = 1.0,
        speed: float = 0.0,
        health: int = 100,
        damage: int = 10,
        cost: int = 0,
        name: str = "default",
    ) -> None:
        self.render_group = render_group
        self.pos = pygame.Vector2(pos)
        self.size = pygame.Vector2(size)
        self.rect = pygame.FRect(*pos, *size)
        self.rot = rot
        self.tex_idx = tex_idx
        self.depth = depth
        self.speed = speed
        self.health = health
        self.damage = damage
        self.cost = cost
        self.name = name
        self._register()

    def set_pos(self, pos: pygame.Vector2 | tuple[float | int, float | int]) -> None:
        self.pos = pygame.Vector2(pos)
        self.rect.topleft = self.pos.x, self.pos.y

    def set_size(self, size: pygame.Vector2 | tuple[float | int, float | int]) -> None:
        self.size = pygame.Vector2(size)
        self.rect.size = self.size.x, self.size.y

    def move(self, dx: int | float, dy: int | float, dt: float) -> None:
        if dx != 0 and dy != 0:
            length = math.sqrt(dx * dx + dy * dy)
            dx /= length
            dy /= length

        self.pos.x += dx * self.speed * dt
        self.pos.y += dy * self.speed * dt
        self.set_pos(self.pos)

    def pack(self) -> tuple[float, float, float, float, float, float, float]:
        return (*self.rect, self.rot, self.tex_idx, self.depth)

    def _register(self) -> None:
        self.render_group.sprites.append(self)

    def delete(self) -> None:
        if self in self.render_group.sprites:
            self.render_group.sprites.remove(self)
