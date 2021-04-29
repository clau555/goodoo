import pygame.mouse

from constants import TILE_SCALE
from displayable import Displayable


class Cursor(Displayable):
    """
    Cursor is a displayable object which is
    displayed every frame at the user mouse position.\n
    """

    def __init__(self) -> None:
        self.__ENABLED_SPRITE: str = "data/sprites/cursor.png"
        self.__DISABLED_SPRITE: str = "data/sprites/cursor_disabled.png"
        super().__init__(pygame.mouse.get_pos(),
                         (TILE_SCALE * 2 // 5, TILE_SCALE * 2 // 5),
                         sprite=self.__ENABLED_SPRITE)

    def disable(self) -> None:
        self.set_sprite(self.__DISABLED_SPRITE)

    def enable(self) -> None:
        self.set_sprite(self.__ENABLED_SPRITE)

    def update(self) -> None:
        self.rect.center = pygame.mouse.get_pos()
