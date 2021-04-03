import math

from pygame.math import Vector2

from displayable import Displayable
from tile import Tile


class Projectile(Displayable):

    def __init__(self, pos: tuple[int, int], size: tuple[int, int], color: tuple[int, int, int],
                 angle: float, speed: float) -> None:

        super(Projectile, self).__init__(pos, size, color)

        # FIXME the line followed by the projectile doesn't match the targeted position
        self.__speed: float = speed
        self.__angle: float = math.radians(angle)
        self.__velocity: Vector2 = Vector2(self.__speed * math.cos(self.__angle),
                                           -self.__speed * math.sin(self.__angle))
        self.alive = True

    def update(self, tiles: list[Tile], delta_time: float) -> None:
        self.rect = self.rect.move(self.__velocity * delta_time)

        # tiles collision
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                self.alive = False

        # TODO entities collision
