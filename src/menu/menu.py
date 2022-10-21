import sys
import time
from dataclasses import replace
from random import random
from typing import Tuple, List

import pygame
from pygame import KEYDOWN, K_ESCAPE, QUIT, MOUSEBUTTONDOWN
from pygame.surface import Surface
from pygame.time import Clock

from src.menu.menu_particles import spawn_menu_particle, update_display_menu_particles
from src.model.constants import BLACK, FONT_TEXT, SCREEN_SIZE, MENU_TITLE, MENU_START, FONT_TITLE, WHITE, TARGET_FPS, \
    FPS, MENU_PARTICLE_SPAWN_RATE, MENU_TEXT_BLINK_SPEED
from src.model.dataclasses import MenuEvents, MenuParticle


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

    while not over:

        clock.tick(FPS)

        now: float = time.time()
        delta_time: float = (now - last_time)
        delta: float = delta_time * TARGET_FPS
        last_time = now

        events: MenuEvents = _update_events(events)
        if events.start:
            over = True

        if random() < MENU_PARTICLE_SPAWN_RATE:
            menu_particles = spawn_menu_particle(menu_particles)

        screen.fill(BLACK)
        menu_particles = update_display_menu_particles(menu_particles, screen, delta)
        _display_title(screen)

        # blinking text
        if timer % 1 < MENU_TEXT_BLINK_SPEED:
            _display_start(screen)

        pygame.display.flip()
        timer += delta_time


def _update_events(events: MenuEvents) -> MenuEvents:
    """
    Update events from pygame event queue inside menu screen.

    :param events: events data
    :return: updated events data
    """
    start: bool = False

    for event in pygame.event.get():

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit("Game ended by user.")
            else:
                start = True

        elif event.type == MOUSEBUTTONDOWN:
            start = True

        elif event.type == QUIT:
            pygame.quit()
            sys.exit()

    return replace(events, start=start)


def _display_title(screen: Surface) -> None:
    """
    Displays title on screen.

    :param screen: screen surface
    """
    title: Surface = FONT_TITLE.render(MENU_TITLE, False, WHITE)
    screen.blit(
        title,
        (SCREEN_SIZE[0] // 2 - title.get_rect().w // 2,
         SCREEN_SIZE[1] / 3 - title.get_rect().h)
    )


def _display_start(screen: Surface) -> None:
    """
    Displays start text on screen.

    :param screen: screen surface
    """
    press_enter: Surface = FONT_TEXT.render(MENU_START, False, WHITE)
    pos: Tuple[int, int] = (
        SCREEN_SIZE[0] // 2 - press_enter.get_rect().w // 2,
        SCREEN_SIZE[1] * 2 / 3 - press_enter.get_rect().h
    )
    screen.blit(press_enter, pos)
