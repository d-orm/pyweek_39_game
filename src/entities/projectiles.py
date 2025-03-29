from typing import TYPE_CHECKING

import pygame

from src.entities.sprite import Sprite

if TYPE_CHECKING:
    from src.scene import Scene


class Projectiles:
    def __init__(
        self,
        scene: "Scene",
        cd_duration: float = 0.5,
        speed: float = 300,
        damage: int = 10,
        size: pygame.Vector2 | tuple[int | float, int | float] = pygame.Vector2(10, 30),
    ) -> None:
        self.scene = scene
        self.render_groups = scene.render_groups
        self.cd_duration = cd_duration
        self.speed = speed
        self.damage = damage
        self.size = pygame.Vector2(size)
        self.cd_timer = 0.0
        self.active_projectiles: list[Sprite] = []
        self.is_shooting = False

    def update(self, player: Sprite, dt: float) -> None:
        if self.cd_timer > 0:
            self.cd_timer -= dt

        if self.is_shooting and self.cd_timer <= 0:
            self.shoot(player)
            self.scene.audio.play_sound(self.scene.sfx["shoot"])
            self.scene.money -= 1
            self.cd_timer = self.cd_duration

        for proj in self.active_projectiles:
            proj.pos.y += proj.speed * dt
            proj.set_pos(proj.pos)

    def shoot(self, player: Sprite) -> None:
        x_pos = player.pos.x + player.size.x / 2 - self.size.x / 2
        y_pos = player.pos.y + player.size.y / 2
        pos = pygame.Vector2(x_pos, y_pos)
        projectile = Sprite(
            render_group=self.render_groups["default"],
            pos=pos,
            size=self.size,
            tex_idx=0,
            depth=8,
            speed=self.speed,
        )
        self.active_projectiles.append(projectile)
