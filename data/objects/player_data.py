from dataclasses import dataclass

from numpy import ndarray, array
from pygame import Rect


@dataclass(frozen=True)
class Player:
    rect: Rect
    velocity: ndarray = array((0, 0))
    on_ground: bool = False
