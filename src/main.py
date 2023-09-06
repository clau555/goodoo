import pygame
from pygame import QUIT, KEYDOWN, MOUSEBUTTONUP, MOUSEBUTTONDOWN, FULLSCREEN, SCALED

from src.game.game import Game
from src.menu.menu import Menu
from src.utils.constants import WINDOW_ICON, WINDOW_TITLE, SCREEN_SIZE


def main(keyboard_layout: str) -> None:
    """
    Handles window creation and screens logic loop.

    :param keyboard_layout: keyboard layout string
    """
    _create_window()
    while True:
        Menu().run()
        Game(keyboard_layout).run()


def _create_window() -> None:
    """
    Creates the window with its proper settings.
    """
    pygame.init()
    pygame.display.set_icon(WINDOW_ICON)
    pygame.display.set_caption(WINDOW_TITLE)
    pygame.display.set_mode(SCREEN_SIZE, FULLSCREEN | SCALED)
    pygame.mouse.set_visible(False)
    pygame.event.set_allowed([QUIT, KEYDOWN, MOUSEBUTTONUP, MOUSEBUTTONDOWN])
