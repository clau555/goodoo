from dataclasses import dataclass, replace, field
from typing import List

from pygame.rect import Rect
from pygame.surface import Surface

from data.utils import GOAL_SPRITES
from data.utils.screen import world_to_screen


@dataclass(frozen=True)
class Goal:
    rect: Rect
    sprites: List[Surface] = field(default_factory=lambda: GOAL_SPRITES)
    current_sprite: float = 0


def update_goal(goal: Goal) -> Goal:
    idx: float = goal.current_sprite + 0.1
    idx = idx % len(goal.sprites)
    return replace(goal, current_sprite=idx)


def display_goal(goal: Goal, screen: Surface) -> None:
    screen.blit(
        goal.sprites[int(goal.current_sprite)],
        world_to_screen(goal.rect.topleft)
    )
