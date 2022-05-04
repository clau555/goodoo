from dataclasses import dataclass, field
from typing import List

from pygame.rect import Rect
from pygame.surface import Surface

from data.utils.constants import GOAL_SPRITES


@dataclass(frozen=True)
class Goal:
    rect: Rect
    sprites: List[Surface] = field(default_factory=lambda: GOAL_SPRITES)
    current_sprite: float = 0
