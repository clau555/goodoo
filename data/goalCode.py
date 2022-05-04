from dataclasses import replace

from pygame.surface import Surface

from data.goalData import Goal
from data.utils.screen import world_to_screen


def update_goal(goal: Goal) -> Goal:
    idx: float = goal.current_sprite + 0.1
    idx = idx % len(goal.sprites)
    return replace(goal, current_sprite=idx)


def display_goal(goal: Goal, screen: Surface) -> None:
    # screen_pos: ndarray = do_camera_offset(world_to_screen(array(goal.rect.topleft)), player)
    screen.blit(goal.sprites[int(goal.current_sprite)], world_to_screen(goal.rect.topleft))
