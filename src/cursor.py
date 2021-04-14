import pygame.mouse

from config import TILE_SCALE
from displayable import Displayable


class Cursor(Displayable):
    """
    Cursor is a displayable object which is
    displayed every frame at the user mouse position.
    """

    def __init__(self) -> None:
        super().__init__(pygame.mouse.get_pos(),
                         (TILE_SCALE * 2 // 5, TILE_SCALE * 2 // 5),
                         sprite="assets/cursor.png",)

    def disable(self) -> None:
        self.set_sprite("assets/cursor_disabled.png")

    def enable(self) -> None:
        self.set_sprite("assets/cursor.png")

    def update(self) -> None:
        self.rect.center = pygame.mouse.get_pos()
