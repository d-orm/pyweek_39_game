import pygame

from src.window.audio.base import Audio


class PygameAudio(Audio[pygame.mixer.Sound]):
    def __init__(self) -> None:
        pygame.mixer.init()

    def load_sound(self, path: str) -> pygame.mixer.Sound:
        return pygame.mixer.Sound(path)

    def load_music(self, path: str) -> pygame.mixer.Sound:
        return pygame.mixer.Sound(path)

    def play_sound(self, sound: pygame.mixer.Sound) -> None:
        sound.play()

    def play_music(self, sound: pygame.mixer.Sound) -> None:
        sound.play(-1)
