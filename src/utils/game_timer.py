import time

from pygame.time import Clock

FPS: int = 60
TARGET_FPS: float = 60.


class GameTimer:
    """
    Class used to track time and between frames and since the start of the game.
    """

    def __init__(self):
        self._clock: Clock = Clock()
        self._last_time: float = time.time()
        self._delta: float = 0
        self._time_elapsed: float = 0

    def update(self):
        self._clock.tick(FPS)

        now: float = time.time()
        delta_time: float = (now - self._last_time)

        self._delta: float = delta_time * TARGET_FPS
        self._time_elapsed += delta_time
        self._last_time = now

    @property
    def delta(self):
        return self._delta

    @property
    def time_elapsed(self):
        return self._time_elapsed

    def reset(self):
        self._last_time = time.time()
