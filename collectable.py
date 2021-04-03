import math

from pygame.math import Vector2

from constants import TILE_SCALE
from displayable import Displayable


class Collectable(Displayable):

    def __init__(self, pos: tuple[int, int], sprite: str) -> None:
        super(Collectable, self).__init__(pos, (int(TILE_SCALE * 2 / 3), int(TILE_SCALE * 2 / 3)), sprite=sprite)
        self.is_available: bool = True
        self.__origin: Vector2 = Vector2(pos)
        self.__counter: int = 0

    def update(self, delta_time: float) -> None:
        # FIXME movements between two collectables can be asynchronous after an entity grabbed one
        self.__counter = (self.__counter + 10) % 360
        self.rect.y = self.__origin.y + (TILE_SCALE / 6) * math.cos(math.radians(self.__counter)) * delta_time
