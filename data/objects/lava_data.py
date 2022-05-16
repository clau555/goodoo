from dataclasses import dataclass

from pygame import Rect


@dataclass(frozen=True)
class Lava:
    y: float
    rect: Rect
