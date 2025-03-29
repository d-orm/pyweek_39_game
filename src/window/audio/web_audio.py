from pyscript.web import audio  # type: ignore

from src.window.audio.base import Audio


class WebAudio(Audio[audio]):
    def load_sound(self, path: str) -> audio:
        return audio(src=path)

    def load_music(self, path: str) -> audio:
        return audio(src=path, loop=True)

    def play_sound(self, sound: audio) -> None:
        sound.play()

    def play_music(self, sound: audio) -> None:
        sound.play()
