import pygame

from config import TILE_SCALE
from displayable import Displayable


class Tile(Displayable):

    def __init__(self, pos: tuple[int, int], is_at_top: bool = False) -> None:
        super(Tile, self).__init__(pos, (TILE_SCALE, TILE_SCALE))
        self.is_at_top = is_at_top

    def display(self) -> None:
        screen = pygame.display.get_surface()
        pygame.draw.rect(screen, (75, 75, 75), self.rect)
        if self.is_at_top:
            pygame.draw.rect(screen, (200, 200, 200), pygame.Rect((self.rect.x, self.rect.y),
                                                                  (TILE_SCALE, TILE_SCALE / 10)))
