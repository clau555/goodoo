from random import random, getrandbits

from numpy import around, ndarray, array
from pygame import Rect
from pygame.surface import Surface
from pygame.transform import flip

from src.utils.constants import GRAVITY, SCREEN_SIZE, PLAYER_SIZE, PLAYER_SPRITE, PLAYER_MAX_V
from src.utils.utils import clamp_vec


class MenuParticle:
    """
    Falling player sprite in the background of the menu screen.
    All of its coordinate system is in screen space.
    """

    def __init__(self):
        self._position: ndarray = self._init_position()
        self._rect: Rect = Rect(tuple(self._position), tuple(PLAYER_SIZE))
        self._velocity: ndarray = array((1 - random() * 2, 0))
        self._flipped: bool = bool(getrandbits(1))

    @staticmethod
    def _init_position() -> ndarray:
        x: int = int(random() * SCREEN_SIZE[0] - PLAYER_SIZE[0])
        y: int = -PLAYER_SIZE[1]
        return array((x, y))

    def update(self, delta: float) -> None:
        """
        Makes the menu particle fall.

        :param delta: delta between two frames
        """
        velocity: ndarray = self._velocity + GRAVITY * delta
        self._velocity = clamp_vec(velocity, PLAYER_MAX_V)
        self._position: ndarray = self._position + self._velocity
        self._rect.topleft = around(self._position)

    def display(self, screen: Surface) -> None:
        """
        Displays a menu particle on screen that has the appearance of a player sprite.

        :param screen: main screen surface
        """
        sprite: Surface = PLAYER_SPRITE if not self._flipped else flip(PLAYER_SPRITE, True, False)
        screen.blit(sprite, around(self._rect.topleft))

    def is_outside_screen(self) -> bool:
        return self._rect.top > SCREEN_SIZE[1]
