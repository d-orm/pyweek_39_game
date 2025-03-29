import os
from typing import TYPE_CHECKING

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from src.rendering.renderer import Renderer
from src.scene import Scene

if TYPE_CHECKING:
    from webwindow import WebWindow  # type: ignore

    from src.window.audio.pygame_audio import PygameAudio
    from src.window.audio.web_audio import WebAudio
    from src.window.pygame_window import PygameWindow


class App:
    def __init__(
        self, window: "PygameWindow | WebWindow", audio: "PygameAudio | WebAudio"
    ) -> None:
        self.window = window
        self.renderer = Renderer(self.window)
        self.scene = Scene(self.renderer, audio)

    def run(self) -> None:
        self.scene.update()
        self.renderer.render()

    async def start(self) -> None:
        await self.window.on_render(self.run)
