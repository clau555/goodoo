from dataclasses import replace

from numpy import ndarray

from pygame.surface import Surface

from data.goalData import Goal


def update_goal(goal: Goal) -> Goal:
    idx: float = goal.current_sprite + 0.1
    idx = idx % len(goal.sprites)
    return replace(goal, current_sprite=idx)


def display_goal(goal: Goal, screen: Surface, camera_offset: ndarray) -> None:
    """
    Displays the goal on the screen and animates it.

    :param goal: goal data
    :param screen: screen surface
    :param camera_offset: camera offset
    """
    screen.blit(goal.sprites[int(goal.current_sprite)], goal.rect.topleft + camera_offset)
