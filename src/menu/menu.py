from random import random

import pygame
from numpy import array, ndarray
from pygame import KEYDOWN, K_ESCAPE, K_UP, K_DOWN, K_RETURN, QUIT
from pygame.mixer import music, Sound
from pygame.surface import Surface

from src.menu.menu_particles import MenuParticle
from src.utils.constants import BLACK, SCREEN_SIZE, FONT_TEXT, WHITE, MENU_TITLE, MENU_BUTTONS_LABELS, \
    MENU_BUTTON_MARGIN, MENU_PARTICLE_SPAWN_RATE, MENU_MUSIC_PATH, SELECT_CHANGE_SOUND, SELECT_SOUND
from src.utils.game_timer import GameTimer
from src.utils.utils import end_program


class Menu:
    """
    Handles the program when running the menu screen.
    """

    def __init__(self):
        self._is_running: bool = True
        self._screen: Surface = pygame.display.get_surface()
        self._particles: list[MenuParticle] = []
        self._selected_index: int = 0
        self._timer = GameTimer()

    def run(self) -> None:

        music.load(MENU_MUSIC_PATH)
        music.play(-1)

        while self._is_running:
            self._timer.update()
            self._update(self._timer.delta)
            self._display()

        music.stop()

    # update -----------------------------------------------------------------------------------------------------------

    def _update(self, delta: float) -> None:
        self._update_from_events()
        if Menu._can_spawn_particle():
            self._particles.append(MenuParticle())
        self._update_particles(delta)

    def _update_from_events(self) -> None:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                self._update_from_input(event.key)
            elif event.type == QUIT:
                end_program()

    def _update_from_input(self, input_key: int) -> None:
        if input_key == K_UP:
            Sound.play(SELECT_CHANGE_SOUND)
            self._update_button_up()

        elif input_key == K_DOWN:
            Sound.play(SELECT_CHANGE_SOUND)
            self._update_button_down()

        elif input_key == K_RETURN:
            Sound.play(SELECT_SOUND)
            if self._selected_index == 0:
                self._is_running = False  # pass to the next screen
            elif self._selected_index == 1:
                end_program()

        elif input_key == K_ESCAPE:
            end_program()

    def _update_button_up(self) -> None:
        self._selected_index = max(0, self._selected_index - 1)

    def _update_button_down(self) -> None:
        self._selected_index = min(len(MENU_BUTTONS_LABELS) - 1, self._selected_index + 1)

    @staticmethod
    def _can_spawn_particle() -> bool:
        return random() < MENU_PARTICLE_SPAWN_RATE

    def _update_particles(self, delta: float) -> None:
        for _, particle in enumerate(self._particles):
            particle: MenuParticle
            particle.update(delta)

            if particle.is_outside_screen():
                index: int = self._particles.index(particle)
                self._particles.pop(index)

    # display ----------------------------------------------------------------------------------------------------------

    def _display(self):
        self._screen.fill(BLACK)
        self._display_particles()
        self._display_title()
        self._display_buttons()
        pygame.display.flip()

    def _display_title(self) -> None:
        x: int = SCREEN_SIZE[0] // 2 - MENU_TITLE.get_rect().w // 2
        y: int = SCREEN_SIZE[1] / 3 - MENU_TITLE.get_rect().h
        self._screen.blit(MENU_TITLE, (x, y))

    def _display_buttons(self) -> None:
        y: int = int(SCREEN_SIZE[1]) // 2

        for i, label in enumerate(MENU_BUTTONS_LABELS):

            button_text: str = label
            if i == self._selected_index:
                if self._timer.time_elapsed % 1 < 0.5:
                    button_text = f"[ {label} ]"
                else:
                    button_text = f"[  {label}  ]"

            button: Surface = FONT_TEXT.render(button_text, False, WHITE)
            x: int = SCREEN_SIZE[0] // 2 - button.get_rect().w // 2
            position: ndarray = array((x, y))

            self._screen.blit(button, position)
            y += button.get_rect().h + MENU_BUTTON_MARGIN

    def _display_particles(self) -> None:
        for _, particle in enumerate(self._particles):
            particle: MenuParticle
            particle.display(self._screen)
