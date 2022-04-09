from dataclasses import dataclass

from pygame.rect import Rect
from pygame.surface import Surface

from data.utils import GOAL_SPRITE
from data.utils.screen import tuple_to_screen


@dataclass(frozen=True)
class Goal:
    rect: Rect
    sprite: Surface = GOAL_SPRITE


def display_goal(goal: Goal, screen: Surface) -> None:
    # TODO animation
    screen.blit(goal.sprite, tuple_to_screen(goal.rect.topleft))
