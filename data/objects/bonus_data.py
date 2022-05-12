from dataclasses import dataclass

from pygame import Rect


@dataclass(frozen=True)
class Bonus:
    rect: Rect
    alive: bool = True
