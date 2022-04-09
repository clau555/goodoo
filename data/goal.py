from dataclasses import dataclass

from pygame.rect import Rect
from pygame.surface import Surface

from data.constants import GOAL_SPRITE


@dataclass(frozen=True)
class Goal:
    rect: Rect
    sprite: Surface = GOAL_SPRITE
