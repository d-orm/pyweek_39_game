import asyncio
from typing import Callable

import pygame

from src.window.inputs_map import Inputs, PygameKeyMap, PygameMouseButtons


class PygameWindow:
    def __init__(
        self,
        width: int,
        height: int,
    ) -> None:
        self.size = width, height
        pygame.init()
        pygame.display.set_mode(self.size, pygame.DOUBLEBUF | pygame.OPENGL)
        self.clock = pygame.time.Clock()
        self.keys = pygame.key.get_pressed()
        self.dt = 0.0
        self.running = True
        self.prev_mouse = self.mouse

    def _update_keys(self) -> None:
        self.keys = pygame.key.get_pressed()
        self.mouse_buttons = pygame.mouse.get_pressed()

    def _get_mapped_key(self, key: Inputs) -> bool | int:
        return PygameKeyMap.get(key, False)

    def key_down(self, key: Inputs) -> bool:
        mapped_key = self._get_mapped_key(key)
        if mapped_key in PygameMouseButtons:
            return self.mouse_buttons[mapped_key]
        return self.keys[mapped_key]

    def key_pressed(self, key: Inputs) -> bool:
        mapped_key = self._get_mapped_key(key)
        if mapped_key in PygameMouseButtons:
            return pygame.mouse.get_just_pressed()[mapped_key]
        return pygame.key.get_just_pressed()[mapped_key]

    def key_released(self, key: Inputs) -> bool:
        mapped_key = self._get_mapped_key(key)
        if mapped_key in PygameMouseButtons:
            return pygame.mouse.get_just_released()[mapped_key]
        return pygame.key.get_just_released()[mapped_key]

    @property
    def frame_time(self) -> float:
        return self.dt

    @property
    def time(self) -> float:
        return pygame.time.get_ticks() / 1000

    @property
    def mouse(self) -> tuple[int, int]:
        return pygame.mouse.get_pos()

    @property
    def mouse_delta(self) -> tuple[int, int]:
        return (
            self.mouse[0] - self.prev_mouse[0],
            self.mouse[1] - self.prev_mouse[1],
        )

    async def on_render(self, render: Callable[[], None]) -> None:
        while self.running:
            self.dt = self.clock.tick(60) / 1000
            self._update_keys()
            render()
            self.prev_mouse = self.mouse
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            pygame.display.flip()
            await asyncio.sleep(0)
