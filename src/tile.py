import pygame

from constants import TILE_SCALE
from displayable import Displayable


class Tile(Displayable):
    """
    A tile is a fixed displayable object that collides with entities and projectiles.
    """

    def __init__(self, pos: tuple[int, int], color: tuple[int, int, int], is_at_top: bool = False) -> None:
        super(Tile, self).__init__(pos, (TILE_SCALE, TILE_SCALE), color=color)
        self.__at_top: bool = is_at_top

    def is_at_top(self) -> bool:
        return self.__at_top

    def set_at_top(self, is_at_top: bool) -> None:
        self.__at_top = is_at_top

    def display(self) -> None:
        screen = pygame.display.get_surface()
        pygame.draw.rect(screen, self.color, self.rect)
        if self.__at_top:
            pygame.draw.rect(screen, (100, 100, 100), pygame.Rect((self.rect.x, self.rect.y),
                                                                  (TILE_SCALE, TILE_SCALE / 20)))
