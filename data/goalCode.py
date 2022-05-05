from dataclasses import replace

from pygame.surface import Surface

from data.goalData import Goal


def update_goal(goal: Goal) -> Goal:
    idx: float = goal.current_sprite + 0.1
    idx = idx % len(goal.sprites)
    return replace(goal, current_sprite=idx)


def display_goal(goal: Goal, screen: Surface) -> None:
    screen.blit(goal.sprites[int(goal.current_sprite)], goal.rect.topleft)
