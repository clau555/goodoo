from dataclasses import dataclass

from numpy import ndarray, array
from pygame import Rect
from pygame.surface import Surface

from data.utils.constants import PLAYER_SPRITE


@dataclass(frozen=True)
class Player:
    rect: Rect
    sprite: Surface = PLAYER_SPRITE
    velocity: ndarray = array((0, 0))
    on_ground: bool = False
