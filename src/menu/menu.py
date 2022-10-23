import time
from dataclasses import replace
from random import random
from typing import List

import pygame
from numpy import ndarray, array
from pygame import KEYDOWN, K_ESCAPE, QUIT, K_DOWN, K_UP, K_RETURN
from pygame.surface import Surface
from pygame.time import Clock

from src.menu.menu_particles import spawn_menu_particle, update_display_menu_particles
from src.model.constants import BLACK, SCREEN_SIZE, MENU_TITLE, TARGET_FPS, \
    FPS, MENU_PARTICLE_SPAWN_RATE, MENU_BUTTONS_LABELS, MENU_BUTTON_MARGIN, FONT_TEXT, WHITE
from src.model.dataclasses import MenuEvents, MenuParticle
from src.model.utils import end_program


def menu() -> None:
    """
    Handles menu screen logic.
    """

    events: MenuEvents = MenuEvents()
    screen: Surface = pygame.display.get_surface()
    over: bool = False

    menu_particles: List[MenuParticle] = []

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

        events: MenuEvents = _update_events(events)
        if events.up:
            idx = max(0, idx - 1)
        elif events.down:
            idx = min(len(MENU_BUTTONS_LABELS) - 1, idx + 1)

        elif events.enter:
            # TODO add settings screen
            if idx == 0:
                over = True
            elif idx == 2:
                end_program()

        if random() < MENU_PARTICLE_SPAWN_RATE:
            menu_particles = spawn_menu_particle(menu_particles)

        screen.fill(BLACK)
        menu_particles = update_display_menu_particles(menu_particles, screen, delta)
        _display_title(screen)
        _display_buttons(screen, idx, timer)

        pygame.display.flip()
        timer += delta_time


def _update_events(events: MenuEvents) -> MenuEvents:
    """
    Update events from pygame event queue inside menu screen.

    :param events: events data
    :return: updated events data
    """
    up: bool = False
    down: bool = False
    enter: bool = False

    for event in pygame.event.get():

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                end_program()
            elif event.key == K_UP:
                up = True
            elif event.key == K_DOWN:
                down = True
            elif event.key == K_RETURN:
                enter = True

        elif event.type == QUIT:
            end_program()

    return replace(events, up=up, down=down, enter=enter)


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


def _display_buttons(screen: Surface, idx: int, timer: float) -> None:
    """
    Displays buttons on screen.

    :type timer:
    :param screen: screen surface
    :param idx: index of the button to highlight
    """
    height = SCREEN_SIZE[1] // 2

    for i, label in enumerate(MENU_BUTTONS_LABELS):

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
