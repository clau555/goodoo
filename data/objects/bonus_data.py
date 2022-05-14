from dataclasses import dataclass

from numpy import ndarray
from pygame import Rect


@dataclass(frozen=True)
class Bonus:
    rect: Rect
    origin: ndarray  # expected to be top left coordinates of rect
    alive: bool = True
