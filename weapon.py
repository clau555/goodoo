import pygame

from collectable import Collectable
from constants import TILE_SCALE
from projectile import Projectile


class Weapon(Collectable):

    MELEE = 0
    RANGE = 1

    def __init__(self, pos: tuple[int, int], sprite: str, weapon_type: int, recoil: float = 0) -> None:
        super(Weapon, self).__init__(pos, sprite)
        self.type: int = weapon_type
        self.recoil: float = recoil

    def action(self, projectiles: list[Projectile]) -> None:

        if self.type == self.RANGE:
            projectiles.append(Projectile(self.rect.center, (TILE_SCALE / 8, TILE_SCALE / 8),
                                          (255, 255, 0), pygame.mouse.get_pos(), TILE_SCALE / 4))

        elif self.type == self.MELEE:
            # TODO weapon melee action
            print("melee action")
