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
#   screen_pos: ndarray = field(init=False)

#   def __post_init__(self):
#       player_screen_size: ndarray = world_to_screen(array(self.rect.size))
#       screen_pos: ndarray = SCREEN_CENTER - player_screen_size // 2
#       object.__setattr__(self, "screen_pos", screen_pos)
