import asyncio
import sys

from src.app import App

SCREEN_SIZE = 1600, 900
is_web = sys.platform in ("emscripten", "wasi")


def run_pyscript() -> None:
    """`python -m scripts.create_pyscript_toml | python -m http.server -d .`"""
    from webwindow import WebWindow  # type: ignore

    from src.window.audio.web_audio import WebAudio

    window = WebWindow(*SCREEN_SIZE)
    audio = WebAudio()
    asyncio.create_task(App(window, audio).start())


def run_native():
    """`python -m main`"""
    from src.window.audio.pygame_audio import PygameAudio
    from src.window.pygame_window import PygameWindow

    window = PygameWindow(*SCREEN_SIZE)
    audio = PygameAudio()
    asyncio.run(App(window, audio).start())


if __name__ == "__main__":
    if is_web:
        run_pyscript()
    else:
        run_native()
