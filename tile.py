from config import TILE_SCALE
from displayable import *


class Tile(Displayable):

    def __init__(self, pos: tuple[int, int]) -> None:
        super(Tile, self).__init__(pos, (TILE_SCALE, TILE_SCALE), color=(255, 255, 255))
