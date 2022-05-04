from dataclasses import dataclass

from numpy import ndarray
from pygame.rect import Rect
from pygame.surface import Surface


@dataclass(frozen=True)
class Tile:
    rect: Rect
    sprite: Surface
    sprite_size: ndarray
