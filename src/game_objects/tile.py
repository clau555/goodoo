import pygame

from src.game_objects.displayable import Displayable
from src.constants import TILE_SCALE


class Tile(Displayable):
    """
    A tile is a fixed displayable object that collides with entities and projectiles.
    """

    def __init__(self, pos: tuple[int, int], color: tuple[int, int, int], is_top: bool = False) -> None:
        super(Tile, self).__init__(pos, (TILE_SCALE, TILE_SCALE), color=color)
        self.__is_top: bool = is_top

    def set_top(self, is_top: bool) -> None:
        self.__is_top = is_top

    def display(self) -> None:
        screen = pygame.display.get_surface()
        pygame.draw.rect(screen, self.color, self.rect)
        if self.__is_top:
            pygame.draw.rect(screen, (100, 100, 100), pygame.Rect((self.rect.x, self.rect.y),
                                                                  (TILE_SCALE, TILE_SCALE / 10)))
