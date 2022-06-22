from dataclasses import dataclass
from typing import List

from numpy import ndarray
from pygame import Rect, Surface


@dataclass(frozen=True)
class Bonus:
    rect: Rect
    origin: ndarray  # expected to be top left coordinates of rect
    lights: List[Surface]
    alive: bool = True
