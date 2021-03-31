import pygame

from config import TILE_SCALE
from displayable import Displayable


class Tile(Displayable):

    def __init__(self, pos: tuple[int, int], color: tuple[int, int, int], is_at_top: bool = False) -> None:
        super(Tile, self).__init__(pos, (TILE_SCALE, TILE_SCALE), color=color)
        self.is_at_top = is_at_top

    def display(self) -> None:
        screen = pygame.display.get_surface()
        pygame.draw.rect(screen, self.color, self.rect)
        if self.is_at_top:
            pygame.draw.rect(screen, (100, 100, 100), pygame.Rect((self.rect.x, self.rect.y),
                                                                  (TILE_SCALE, TILE_SCALE / 20)))
