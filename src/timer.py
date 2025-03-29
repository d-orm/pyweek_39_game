from typing import Callable


class Timer:
    def __init__(
        self,
        name: str,
        duration: float,
        num_repeats: int,
        callback: Callable,
        callback_args: tuple = (),
    ):
        self.name = name
        self.duration = duration
        self.num_repeats = num_repeats
        self.execution_count = 0
        self.callback = callback
        self.callback_args = callback_args
        self.elapsed = 0.0
        self.done = False

    def update(self, dt: float) -> None:
        self.elapsed += dt
        if self.elapsed >= self.duration:
            self.callback(*self.callback_args)
            self.execution_count += 1
            if self.num_repeats > 0 and self.execution_count >= self.num_repeats:
                self.stop()
            self.elapsed = 0.0

    def stop(self) -> None:
        self.done = True
