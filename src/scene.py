import random
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

import numpy as np

from src.entities.projectiles import Projectiles
from src.entities.sprite import Sprite
from src.entities.text_line import TextLine
from src.timer import Timer
from src.window.inputs_map import Inputs

if TYPE_CHECKING:
    from src.rendering.renderer import Renderer
    from src.window.audio.base import Audio


@dataclass
class LevelData:
    datastream_speed: int
    obstacles_freq: float
    obstacles_speed_range: tuple[int, int]


LEVELS = {
    1: LevelData(
        datastream_speed=250,
        obstacles_freq=2.0,
        obstacles_speed_range=(150, 300),
    ),
    2: LevelData(
        datastream_speed=350,
        obstacles_freq=1.5,
        obstacles_speed_range=(200, 350),
    ),
    3: LevelData(
        datastream_speed=450,
        obstacles_freq=1.0,
        obstacles_speed_range=(250, 400),
    ),
    4: LevelData(
        datastream_speed=550,
        obstacles_freq=0.8,
        obstacles_speed_range=(300, 450),
    ),
    5: LevelData(
        datastream_speed=650,
        obstacles_freq=0.6,
        obstacles_speed_range=(350, 500),
    ),
    6: LevelData(
        datastream_speed=750,
        obstacles_freq=0.4,
        obstacles_speed_range=(400, 550),
    ),
}


class Scene:
    def __init__(self, renderer: "Renderer", audio: "Audio") -> None:
        self.renderer = renderer
        self.audio = audio
        self.load_sfx()
        self.window = renderer.window
        self.render_groups = renderer.render_groups
        self.music_started = False
        self.paused = True
        self.power_ups_panel_active = False
        self.intro_panel_active = True
        self.game_over = False
        self.game_over_panel_active = False
        self.time = 0.0
        self.money = 0
        self.current_level = 1
        self.max_move_speed = 1000
        self.score = 0
        self.enemies_killed = 0
        self.network_breaches = 0
        self.bonus_score = 0
        self.final_score = 0
        self.datastream_speed = LEVELS[self.current_level].datastream_speed
        self.obstacles_speed_range = LEVELS[self.current_level].obstacles_speed_range
        self.obstacles_freq = LEVELS[self.current_level].obstacles_freq
        self.level_increase_freq = 30
        self.ui_panel_height = self.window.size[1] / 8
        self.circuit_board_width = self.window.size[0] // 8
        self.circuit_board_speed = self.datastream_speed / 8
        self.obstacles: list[Sprite] = []
        self.timers: dict[str, Timer] = {}
        self.collided_obstacles: list[Sprite] = []
        self.projectiles = Projectiles(self)
        self.create_entities()
        self.add_timer("add_obstacle", self.obstacles_freq, 0, self.add_obstacle)
        self.add_timer(
            "increment_level", self.level_increase_freq, 0, self.increment_level
        )

    def load_sfx(self) -> None:
        self.sfx = {
            "explosion": self.audio.load_sound("src/assets/sfx/explosion.ogg"),
            "shoot": self.audio.load_sound("src/assets/sfx/laserShoot.ogg"),
            "power_up": self.audio.load_sound("src/assets/sfx/pickupCoin.ogg"),
            "hurt": self.audio.load_sound("src/assets/sfx/hitHurt.ogg"),
            "music": self.audio.load_music("src/assets/sfx/Galactic Lights.ogg"),
        }

    def update(self):
        self.update_controls()
        if self.intro_panel_active:
            return
        if not self.music_started:
            self.audio.play_music(self.sfx["music"])
            self.music_started = True
        self.update_game_over_panel()
        if self.player.health <= 0:
            self.player.health = 0
            self.update_ui_texts()
            self.game_over = True
        if self.game_over:
            self.game_over_panel_active = True
            self.bonus_score = self.money + self.time
            self.final_score = self.score + self.bonus_score
            self.paused = True
            return
        self.update_ui_texts()
        self.update_intro_panel()
        self.update_power_ups_panel()
        if self.paused:
            return
        self.time += self.window.frame_time
        self.money += self.window.frame_time
        self.update_timers()
        self.update_bg(
            self.datastream_bg_1, self.datastream_bg_2, self.datastream_speed
        )
        self.update_bg(
            self.left_circuit_board_bg_1,
            self.left_circuit_board_bg_2,
            self.circuit_board_speed,
        )
        self.update_bg(
            self.right_circuit_board_bg_1,
            self.right_circuit_board_bg_2,
            self.circuit_board_speed,
        )
        self.update_obstacles()
        self.update_player()
        self.update_player_collisions()
        self.update_projectiles()

    def update_game_over_panel(self) -> None:
        if self.game_over_panel_active:
            self.game_over_panel.set_size(self.game_over_panel_size)
            for text in self.game_over_texts:
                text.visible = True
                text.update()
        else:
            self.game_over_panel.set_size((0, 0))

    def update_intro_panel(self) -> None:
        if self.intro_panel_active:
            self.intro_panel.set_size(self.renderer.textures.intro_panel_size)
            self.paused = True
        else:
            self.intro_panel.set_size((0, 0))
            self.paused = False

    def update_player(self) -> None:
        dt = self.window.frame_time
        dx, dy = 0, 0
        if self.window.key_down(Inputs.ArrowUp):
            dy = -1
        if self.window.key_down(Inputs.ArrowDown):
            dy = 1
        if self.window.key_down(Inputs.ArrowLeft):
            dx = -1
        if self.window.key_down(Inputs.ArrowRight):
            dx = 1
        self.player.move(dx, dy, dt)

        if self.player.pos.x < self.circuit_board_width:
            self.player.pos.x = self.circuit_board_width
        elif (
            self.player.pos.x
            > self.window.size[0] - self.circuit_board_width - self.player.size.x
        ):
            self.player.pos.x = (
                self.window.size[0] - self.circuit_board_width - self.player.size.x
            )
        if self.player.pos.y < self.ui_panel_height:
            self.player.pos.y = self.ui_panel_height
        elif self.player.pos.y > self.window.size[1] - self.player.size.y:
            self.player.pos.y = self.window.size[1] - self.player.size.y

        self.player.set_pos(self.player.pos)

    def restart_game(self) -> None:
        self.score = 0
        self.bonus_score = 0
        self.enemies_killed = 0
        self.network_breaches = 0
        self.final_score = 0
        self.game_over = False
        self.game_over_panel_active = False
        for render_group in self.render_groups.values():
            render_group.sprites.clear()
        self.obstacles.clear()
        self.collided_obstacles.clear()
        self.timers.clear()
        self.projectiles.active_projectiles.clear()
        self.create_entities()
        self.time = 0
        self.intro_panel_active = True
        self.money = 0
        self.current_level = 1
        self.datastream_speed = LEVELS[self.current_level].datastream_speed
        self.obstacles_speed_range = LEVELS[self.current_level].obstacles_speed_range
        self.obstacles_freq = LEVELS[self.current_level].obstacles_freq
        self.add_timer("add_obstacle", self.obstacles_freq, 0, self.add_obstacle)
        self.add_timer(
            "increment_level", self.level_increase_freq, 0, self.increment_level
        )

    def update_controls(self):
        if self.window.key_pressed(Inputs.Space) and self.intro_panel_active:
            self.intro_panel_active = False
            self.projectiles.cd_timer = 0.5
            self.paused = False
        if self.window.key_pressed(Inputs.Space) and self.game_over:
            self.restart_game()
        if self.window.key_down(Inputs.Space) and not self.paused and self.money >= 1:
            self.projectiles.is_shooting = True
        else:
            self.projectiles.is_shooting = False
        if self.window.key_pressed(Inputs.KeyP):
            self.paused = not self.paused
        if self.window.key_pressed(Inputs.KeyF):
            self.power_ups_panel_active = not self.power_ups_panel_active

        if self.power_ups_panel_active:
            if self.window.key_pressed(Inputs.Digit1):
                if self.money >= 50 and self.player.speed < self.max_move_speed:
                    self.player.speed *= 1.1
                    self.money -= 50
                    self.audio.play_sound(self.sfx["power_up"])
            if self.window.key_pressed(Inputs.Digit2):
                if self.money >= 50:
                    self.projectiles.cd_duration *= 0.9
                    self.money -= 50
                    self.audio.play_sound(self.sfx["power_up"])
            if self.window.key_pressed(Inputs.Digit3):
                if self.money >= 100:
                    self.player.health = 100
                    self.money -= 100
                    self.audio.play_sound(self.sfx["power_up"])
            if self.window.key_pressed(Inputs.Space):
                self.power_ups_panel_active = False
                self.projectiles.cd_timer = 0.5

    def update_power_ups_panel(self):
        if self.power_ups_panel_active:
            self.power_ups_panel.set_size(self.power_ups_panel_size)
            for button in self.power_up_buttons:
                button.set_size(self.power_up_button_size)
                if (
                    button.name == "move_speed"
                    and (self.player.speed) >= self.max_move_speed
                ):
                    button.tex_idx = 2
                elif self.money >= button.cost:
                    button.tex_idx = 1
                else:
                    button.tex_idx = 0
            for text in self.power_up_texts:
                text.visible = True
                text.update()
            self.paused = True
        else:
            self.power_ups_panel.set_size((0, 0))
            for button in self.power_up_buttons:
                button.set_size((0, 0))
            for text in self.power_up_texts:
                text.visible = False
                text.update()
            self.paused = False

    def update_projectiles(self) -> None:
        self.projectiles.update(self.player, self.window.frame_time)
        projs_to_remove: list[Sprite] = []
        for proj in self.projectiles.active_projectiles:
            if proj.pos.y > self.window.size[1]:
                projs_to_remove.append(proj)
                continue
            for obstacle in self.obstacles:
                if proj.rect.colliderect(obstacle.rect):
                    obstacle.health -= proj.damage
                    projs_to_remove.append(proj)
                    self.audio.play_sound(self.sfx["explosion"])

        for proj in projs_to_remove:
            self.projectiles.active_projectiles.remove(proj)
            proj.delete()

    def update_ui_texts(self):
        # self.fps_text.update()
        self.level_text.update()
        self.score_text.update()
        self.health_text.update()
        self.money_text.update()
        self.move_speed_text.update()
        self.reload_speed_text.update()
        if self.money >= 50:
            self.get_upgrade_text.update()

    def update_bg(self, bg_1: Sprite, bg_2: Sprite, speed: int) -> None:
        window_height = self.window.size[1]
        delta = speed * self.window.frame_time

        bg_1.pos.y -= delta
        bg_2.pos.y -= delta

        if bg_1.pos.y < -window_height:
            bg_1.pos.y += 2 * window_height
        if bg_2.pos.y < -window_height:
            bg_2.pos.y += 2 * window_height

        if abs(abs(bg_1.pos.y - bg_2.pos.y) - window_height) > 1:
            if bg_1.pos.y < bg_2.pos.y:
                bg_2.pos.y = bg_1.pos.y + window_height
            else:
                bg_1.pos.y = bg_2.pos.y + window_height

        bg_1.set_pos(bg_1.pos)
        bg_2.set_pos(bg_2.pos)

    def update_obstacles(self) -> None:
        obs_to_remove: list[Sprite] = []
        for obstacle in self.obstacles:
            obstacle.rot = 10 * np.sin(self.time * 10) if obstacle.rot < 10 else 10

            if obstacle.health <= 0:
                obs_to_remove.append(obstacle)
                obstacle.delete()
                self.enemies_killed += 1
                self.score += 10
                self.money += 10
                continue

            delta = obstacle.speed * self.window.frame_time
            obstacle.set_pos((obstacle.pos.x, obstacle.pos.y - delta))
            if obstacle.pos.y < -obstacle.size[1]:
                obs_to_remove.append(obstacle)
                obstacle.delete()
                self.network_breaches += 1
                self.player.health -= 5
                self.audio.play_sound(self.sfx["hurt"])

        for obstacle in obs_to_remove:
            self.obstacles.remove(obstacle)
            if obstacle in self.collided_obstacles:
                self.collided_obstacles.remove(obstacle)

    def update_player_pos(self) -> None:
        player_size_x, player_size_y = self.player.size
        window_size_x, window_size_y = self.window.size
        offset = self.player.size / 2
        pos = self.window.mouse - offset

        if pos.x < self.circuit_board_width:
            pos.x = self.circuit_board_width
        elif pos.x > window_size_x - self.circuit_board_width - player_size_x:
            pos.x = window_size_x - self.circuit_board_width - player_size_x
        if pos.y < self.ui_panel_height:
            pos.y = self.ui_panel_height
        elif pos.y > window_size_y - player_size_y:
            pos.y = window_size_y - player_size_y
        self.player.set_pos(pos)

    def update_player_collisions(self) -> None:
        for obstacle in self.obstacles:
            if obstacle in self.collided_obstacles:
                continue
            if self.player.rect.colliderect(obstacle.rect):
                self.collided_obstacles.append(obstacle)
                self.player.health -= 10
                self.audio.play_sound(self.sfx["hurt"])

    def update_timers(self):
        for timer in self.timers.values():
            timer.update(self.window.frame_time)

    def create_entities(self) -> None:
        self.create_player()
        self.create_backgrounds()
        self.create_ui_panel()
        self.create_ui_texts()
        self.create_power_ups_panel()
        self.create_power_up_buttons()
        self.create_all_power_up_texts()
        self.create_intro_panel()
        self.create_game_over_panel()
        self.create_game_over_texts()

    def create_player(self) -> None:
        player_img_size = self.renderer.textures.robot_img_size
        player_scale = 0.15
        player_size = (
            player_img_size[0] * player_scale,
            player_img_size[1] * player_scale,
        )
        player_pos = (
            self.window.size[0] // 2 - player_size[0] // 2,
            self.ui_panel_height + player_size[1],
        )
        self.player = Sprite(
            render_group=self.render_groups["player"],
            pos=player_pos,
            size=player_size,
            tex_idx=0,
            depth=3,
            speed=500,
        )

    def create_backgrounds(self) -> None:
        self.datastream_bg_1 = Sprite(
            render_group=self.render_groups["datastream"],
            pos=(0, 0),
            size=self.window.size,
            depth=1,
        )
        self.datastream_bg_2 = Sprite(
            render_group=self.render_groups["datastream"],
            pos=(0, self.window.size[1]),
            size=self.window.size,
            depth=1,
        )
        self.left_circuit_board_bg_1 = Sprite(
            render_group=self.render_groups["circuit_board"],
            pos=(0, 0),
            size=(self.circuit_board_width, self.window.size[1]),
            tex_idx=0,
            depth=2,
        )
        self.left_circuit_board_bg_2 = Sprite(
            render_group=self.render_groups["circuit_board"],
            pos=(0, self.window.size[1]),
            size=(self.circuit_board_width, self.window.size[1]),
            tex_idx=2,
            depth=2,
        )
        self.right_circuit_board_bg_1 = Sprite(
            render_group=self.render_groups["circuit_board"],
            pos=(self.window.size[0] - self.circuit_board_width, 0),
            size=(self.circuit_board_width, self.window.size[1]),
            tex_idx=1,
            depth=2,
        )
        self.right_circuit_board_bg_2 = Sprite(
            render_group=self.render_groups["circuit_board"],
            pos=(self.window.size[0] - self.circuit_board_width, self.window.size[1]),
            size=(self.circuit_board_width, self.window.size[1]),
            tex_idx=3,
            depth=2,
        )

    def create_ui_panel(self) -> None:
        self.ui_panel = Sprite(
            render_group=self.render_groups["ui_panel"],
            pos=(0, 0),
            size=(self.window.size[0], self.ui_panel_height),
            tex_idx=0,
            depth=9,
        )

    def create_game_over_texts(self) -> None:
        panel_pos = self.game_over_panel_pos
        text_callbacks = [
            lambda: "GAME OVER!",
            lambda: f"Enemies Killed: {self.enemies_killed}",
            lambda: f"Network Breaches: {self.network_breaches}",
            lambda: f"Time Survived: {self.time:.0f} seconds",
            lambda: f"Money Remaining: {self.money:.0f}",
            lambda: f"Score: {self.score:.0f}",
            lambda: f"Bonus Score (money + time): {self.bonus_score:.0f}",
            lambda: f"Final Score: {self.final_score:.0f}",
            lambda: "Press SPACE to restart",
        ]
        text_offsets = (
            (10, 10),
            (10, 48 + 38),
            (10, 86 + 38),
            (10, 124 + 38),
            (10, 162 + 38),
            (10, 200 + 38),
            (10, 238 + 38),
            (10, 276 + 38),
            (10, 314 + 38 + 38),
        )

        self.game_over_texts: list[TextLine] = []
        for idx, callback in enumerate(text_callbacks):
            pos = (
                panel_pos[0] + text_offsets[idx][0],
                panel_pos[1] + text_offsets[idx][1],
            )
            self.game_over_texts.append(self.create_text_line(pos, callback))

    def create_ui_texts(self) -> None:
        # self.fps_text = self.create_text_line(
        #     pos=(10, 10),
        #     callback=lambda: f"FPS: {self.renderer.avg_fps:.1f}",
        # )
        self.level_text = self.create_text_line(
            pos=(10, 10),
            callback=lambda: f"Level: {self.current_level if self.current_level < len(LEVELS) else 'MAX'}",
        )
        self.score_text = self.create_text_line(
            pos=(10, 48),
            callback=lambda: f"Score: {self.score:.0f}",
        )
        self.money_text = self.create_text_line(
            pos=(250, 48),
            callback=lambda: f"Money: ${self.money:.0f}",
        )
        self.health_text = self.create_text_line(
            pos=(250, 10),
            callback=lambda: f"Health: {self.player.health:.0f}",
        )
        self.get_upgrade_text = self.create_text_line(
            pos=(self.window.size[0] // 2 - 250, 10),
            callback=lambda: f"Get Upgrade! (Press F)",
        )
        self.reload_speed_text = self.create_text_line(
            pos=(self.window.size[0] - 450, 10),
            callback=lambda: f"Reload Speed: {1 / self.projectiles.cd_duration:.2f}",
        )
        self.move_speed_text = self.create_text_line(
            pos=(self.window.size[0] - 450, 48),
            callback=lambda: f"Move Speed: {self.player.speed / 100:.2f}",
        )

    def create_power_ups_panel(self) -> None:
        self.power_ups_panel_size = (self.window.size[0] // 2, self.window.size[1] // 2)
        self.power_ups_panel_pos = (
            self.window.size[0] // 2 - self.power_ups_panel_size[0] // 2,
            self.window.size[1] // 2 - self.power_ups_panel_size[1] // 2,
        )
        self.power_ups_panel = Sprite(
            render_group=self.render_groups["default"],
            pos=self.power_ups_panel_pos,
            size=self.power_ups_panel_size,
            tex_idx=2,
            depth=9,
        )

    def create_power_up_buttons(self) -> None:
        self.power_up_button_size = (150, 150)

        self.center_power_up_button_pos = (
            int(self.power_ups_panel.rect.centerx - self.power_up_button_size[0] // 2),
            int(self.power_ups_panel.rect.centery - self.power_up_button_size[1] // 2),
        )
        self.left_power_up_button_pos = (
            self.center_power_up_button_pos[0] - self.power_up_button_size[0] - 50,
            self.center_power_up_button_pos[1],
        )
        self.right_power_up_button_pos = (
            self.center_power_up_button_pos[0] + self.power_up_button_size[0] + 50,
            self.center_power_up_button_pos[1],
        )

        self.center_power_up_button = Sprite(
            render_group=self.render_groups["default"],
            pos=self.center_power_up_button_pos,
            size=(0, 0),
            depth=10,
            cost=50,
        )
        self.left_power_up_button = Sprite(
            render_group=self.render_groups["default"],
            pos=self.left_power_up_button_pos,
            size=(0, 0),
            depth=10,
            cost=50,
            name="move_speed",
        )
        self.right_power_up_button = Sprite(
            render_group=self.render_groups["default"],
            pos=self.right_power_up_button_pos,
            size=(0, 0),
            depth=10,
            cost=100,
        )
        self.power_up_buttons = [
            self.center_power_up_button,
            self.left_power_up_button,
            self.right_power_up_button,
        ]

    def create_all_power_up_texts(self) -> None:
        self.power_up_texts: list[TextLine] = []
        x_offsets = [(35, 35, 35, 25, -2), (35, 35, 15, 25, -2), (15, 35, 15, 25, -2)]
        texts = [
            ("-$50", "+10%", "Move", "Speed", "Press[1]"),
            ("-$50", "+10%", "Reload", "Speed", "Press[2]"),
            ("-$100", "Full", "Health", "Regen", "Press[3]"),
        ]
        button_positions = [
            self.left_power_up_button_pos,
            self.center_power_up_button_pos,
            self.right_power_up_button_pos,
        ]
        for idx, button_pos in enumerate(button_positions):
            self.power_up_texts.extend(
                self.create_power_up_button_texts(
                    button_pos, texts[idx], x_offsets[idx]
                )
            )

    def create_power_up_button_texts(
        self,
        button_pos: tuple[int, int],
        text_contents: tuple[str, str, str, str, str],
        text_x_offsets: tuple[int, int, int, int, int],
    ) -> list[TextLine]:
        y_offsets = (-50, 10, 50, 90, 160)

        line_1_text_pos = (
            button_pos[0] + text_x_offsets[0],
            button_pos[1] + y_offsets[0],
        )
        line_2_text_pos = (
            button_pos[0] + text_x_offsets[1],
            button_pos[1] + y_offsets[1],
        )
        line_3_text_pos = (
            button_pos[0] + text_x_offsets[2],
            button_pos[1] + y_offsets[2],
        )
        line_4_text_pos = (
            button_pos[0] + text_x_offsets[3],
            button_pos[1] + y_offsets[3],
        )
        line_5_text_pos = (
            button_pos[0] + text_x_offsets[4],
            button_pos[1] + y_offsets[4],
        )

        lines = [
            self.create_text_line(line_1_text_pos, lambda: text_contents[0]),
            self.create_text_line(line_2_text_pos, lambda: text_contents[1]),
            self.create_text_line(line_3_text_pos, lambda: text_contents[2]),
            self.create_text_line(line_4_text_pos, lambda: text_contents[3]),
            self.create_text_line(line_5_text_pos, lambda: text_contents[4]),
        ]
        return lines

    def create_text_line(self, pos: tuple[int, int], callback: Callable) -> TextLine:
        return TextLine(
            callback=callback,
            render_group=self.render_groups["font"],
            font_size=self.renderer.textures.font_size,
            font_idx_map=self.renderer.textures.font_idx_map,
            pos=pos,
            depth=11,
        )

    def create_intro_panel(self) -> None:
        pos = (
            self.window.size[0] // 2 - self.renderer.textures.intro_panel_size[0] // 2,
            self.window.size[1] // 2 - self.renderer.textures.intro_panel_size[1] // 2,
        )
        self.intro_panel = Sprite(
            render_group=self.render_groups["intro_panel"],
            pos=pos,
            size=self.renderer.textures.intro_panel_size,
            tex_idx=4,
            depth=12,
        )

    def create_game_over_panel(self) -> None:
        self.game_over_panel_size = (self.window.size[0] // 2, self.window.size[1] // 2)
        self.game_over_panel_pos = (
            self.window.size[0] // 2 - self.game_over_panel_size[0] // 2,
            self.window.size[1] // 2 - self.game_over_panel_size[1] // 2,
        )
        self.game_over_panel = Sprite(
            render_group=self.render_groups["ui_panel"],
            pos=self.game_over_panel_pos,
            size=self.game_over_panel_size,
            tex_idx=0,
            depth=9,
        )

    def add_timer(
        self,
        name: str,
        duration: float,
        num_repeats: int,
        callback: Callable,
        callback_args: tuple = (),
    ) -> None:
        self.timers[name] = Timer(name, duration, num_repeats, callback, callback_args)

    def add_obstacle(self) -> None:
        obstacle_id = random.choice(
            list(self.renderer.textures.obstacle_textures.keys())
        )
        size = self.renderer.textures.obstacle_sizes[obstacle_id]
        pos = (
            random.randint(
                self.circuit_board_width,
                self.window.size[0] - self.circuit_board_width - size[0],
            ),
            self.window.size[1],
        )
        speed = random.randint(*self.obstacles_speed_range)
        self.obstacles.append(
            Sprite(
                render_group=self.render_groups[obstacle_id],
                pos=pos,
                size=size,
                depth=4,
                speed=speed,
                health=20,
            )
        )

    def increment_level(self) -> None:
        if self.current_level < len(LEVELS):
            self.current_level += 1
        self.datastream_speed = LEVELS[self.current_level].datastream_speed
        self.obstacles_speed_range = LEVELS[self.current_level].obstacles_speed_range
        self.obstacles_freq = LEVELS[self.current_level].obstacles_freq
        self.timers["add_obstacle"].stop()
        self.add_timer("add_obstacle", self.obstacles_freq, 0, self.add_obstacle)
        self.money += 100
