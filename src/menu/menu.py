import time
from random import random

import pygame
from numpy import array, ndarray
from pygame import KEYDOWN, K_ESCAPE, K_UP, K_DOWN, K_RETURN, QUIT
from pygame.surface import Surface
from pygame.time import Clock

from src.menu.menu_particles import spawn_menu_particle, update_display_menu_particles
from src.model.constants import BLACK, SCREEN_SIZE, MENU_TITLE, TARGET_FPS, \
    FPS, MENU_PARTICLE_SPAWN_RATE, MENU_BUTTONS_LABELS, FONT_TEXT, WHITE, MENU_BUTTON_MARGIN
from src.model.dataclasses import MenuParticle
from src.model.types import MenuEvent
from src.model.utils import end_program


def menu() -> None:
    """
    Handles menu screen logic.
    """
    screen: Surface = pygame.display.get_surface()
    over: bool = False

    menu_particles: list[MenuParticle] = []

    clock: Clock = Clock()
    last_time: float = time.time()
    timer: float = 0

    idx: int = 0  # current selected button index

    while not over:

        clock.tick(FPS)

        now: float = time.time()
        delta_time: float = (now - last_time)
        delta: float = delta_time * TARGET_FPS
        last_time = now

        event: MenuEvent = _menu_event()
        idx = _update_button_idx(idx, event, len(MENU_BUTTONS_LABELS))

        if event == MenuEvent.ENTER:
            if idx == 0:
                over = True
            elif idx == 1:
                end_program()

        if random() < MENU_PARTICLE_SPAWN_RATE:
            menu_particles = spawn_menu_particle(menu_particles)

        screen.fill(BLACK)
        menu_particles = update_display_menu_particles(menu_particles, screen, delta)
        _display_title(screen)
        _display_buttons(MENU_BUTTONS_LABELS, SCREEN_SIZE[1] // 2, screen, idx, timer)

        pygame.display.flip()
        timer += delta_time


def _menu_event() -> MenuEvent:
    """
    Get current frame menu event.

    :return: menu event enum
    """
    for event in pygame.event.get():

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                end_program()
            if event.key == K_UP:
                return MenuEvent.UP
            if event.key == K_DOWN:
                return MenuEvent.DOWN
            if event.key == K_RETURN:
                return MenuEvent.ENTER

        elif event.type == QUIT:
            end_program()


def _update_button_idx(idx: int, event: MenuEvent, n: int) -> int:
    """
    Update button index based on frame event.

    :param idx: current button index
    :param event: menu event enum
    :param n: number of buttons
    :return: updated button index
    """
    if event == MenuEvent.UP:
        return max(0, idx - 1)
    if event == MenuEvent.DOWN:
        return min(n - 1, idx + 1)
    return idx


def _display_title(screen: Surface) -> None:
    """
    Displays title on screen.

    :param screen: screen surface
    """
    screen.blit(
        MENU_TITLE,
        (SCREEN_SIZE[0] // 2 - MENU_TITLE.get_rect().w // 2,
         SCREEN_SIZE[1] / 3 - MENU_TITLE.get_rect().h)
    )


def _display_buttons(buttons_labels: list[str], starting_height: int, screen: Surface, idx: int, timer: float) -> None:
    """
    Displays button list on screen.

    :param buttons_labels: list of buttons labels
    :param starting_height: height of the most upper button
    :type timer: game timer
    :param screen: screen surface
    :param idx: index of the button to highlight
    """
    height: int = starting_height

    for i, label in enumerate(buttons_labels):

        label_: str = label
        if i == idx:
            if timer % 1 < 0.5:
                label_ = f"[ {label} ]"
            else:
                label_ = f"[  {label}  ]"

        button: Surface = FONT_TEXT.render(label_, False, WHITE)
        pos: ndarray = array((SCREEN_SIZE[0] // 2 - button.get_rect().w // 2, height))

        screen.blit(button, pos)

        height += button.get_rect().h + MENU_BUTTON_MARGIN
