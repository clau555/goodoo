from dataclasses import dataclass

from numpy import ndarray, zeros
from pygame import Rect


@dataclass(frozen=True)
class Player:
    pos: ndarray
    rect: Rect
    velocity: ndarray = zeros(2, dtype=float)
    on_ground: bool = False
