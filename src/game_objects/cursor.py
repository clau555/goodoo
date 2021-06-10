import pygame.mouse

from src.game_objects.displayable import Displayable
from src.constants import TILE_SCALE


class Cursor(Displayable):
    """
    Cursor is a displayable object which is
    displayed every frame at the user mouse position.\n
    """

    ENABLED_SPRITE: str = "data/sprites/cursor.png"
    DISABLED_SPRITE: str = "data/sprites/cursor_disabled.png"

    def __init__(self) -> None:
        super().__init__(pygame.mouse.get_pos(),
                         (TILE_SCALE * 2 // 5, TILE_SCALE * 2 // 5),
                         sprite=self.ENABLED_SPRITE)

    def disable(self) -> None:
        self.set_sprite(self.DISABLED_SPRITE)

    def enable(self) -> None:
        self.set_sprite(self.ENABLED_SPRITE)

    def update(self) -> None:
        self.rect.center = pygame.mouse.get_pos()
