from config import GRAVITY, COLLISION_TOLERANCE, TILE_SCALE
from displayable import Displayable
from tile import Tile
from weapon import Weapon


class Entity(Displayable):

    def __init__(self, pos: tuple[int, int], size: tuple[int, int], sprite: str = None,
                 velocity_max: tuple[int, int] = (int(TILE_SCALE * 0.075), int(TILE_SCALE * 0.075)),
                 has_gravity: bool = True) -> None:
        super().__init__(pos, size, sprite)
        self._velocity: list[int, int] = [0, 0]
        self.velocity_max: tuple[int, int] = velocity_max
        self.has_gravity: bool = has_gravity
        self._is_on_ground: bool = False
        self.direction: list[int, int] = [0, 0]
        self.right: bool = False
        self.left: bool = False
        self.up: bool = False
        self.down: bool = False
        self.weapon: Weapon = None

    def update(self, direction_pos: tuple[int, int], tiles: list[Tile],
               weapons: list[Weapon], delta_time: float) -> None:

        self._velocity = [0, 0] if not self.has_gravity else self._velocity

        # movements from controls
        self._velocity[0] = 0

        if self.left and not self.right:
            self._velocity[0] = -self.velocity_max[0]
        elif self.right and not self.left:
            self._velocity[0] = self.velocity_max[0]

        if self.has_gravity:
            if self.up and self._is_on_ground:
                self._velocity[1] -= TILE_SCALE / 4
        else:
            if self.up and not self.down:
                self._velocity[1] = -self.velocity_max[1]
            elif self.down and not self.up:
                self._velocity[1] = self.velocity_max[1]

        # gravity
        if self.has_gravity:
            self._velocity[1] += 1 if self._velocity[1] <= GRAVITY else 0

        # x axis movement execution
        self.rect.x += int(self._velocity[0] * delta_time)

        # x axis collisions
        for tile in tiles:
            if self.rect.colliderect(tile.rect):

                # right collision
                if abs(self.rect.right - tile.rect.left) < COLLISION_TOLERANCE:
                    self.rect.right = tile.rect.left
                    self._velocity[0] = 0

                # left collision
                if abs(self.rect.left - tile.rect.right) < COLLISION_TOLERANCE:
                    self.rect.left = tile.rect.right
                    self._velocity[0] = 0

        # y axis movement execution
        self.rect.y += int(self._velocity[1] * delta_time)

        self._is_on_ground = False

        # y axis collisions
        for tile in tiles:
            if self.rect.colliderect(tile.rect):

                # bottom collision
                if abs(self.rect.bottom - tile.rect.top) < COLLISION_TOLERANCE:
                    self.rect.bottom = tile.rect.top
                    self._velocity[1] = 0
                    self._is_on_ground = True

                # top collision
                if abs(self.rect.top - tile.rect.bottom) < COLLISION_TOLERANCE:
                    self.rect.top = tile.rect.bottom
                    self._velocity[1] = 0

        # direction
        self.direction[0] = direction_pos[0] - self.rect.centerx
        self.direction[1] = direction_pos[1] - self.rect.centery

        # item grabbing
        for weapon in weapons:
            if self.rect.colliderect(weapon.rect):
                self.weapon = weapon
                weapon.is_active = False
