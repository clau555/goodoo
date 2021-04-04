import pygame

from collectable import Collectable
from constants import TILE_SCALE
from projectile import Projectile


class Weapon(Collectable):

    MELEE = 0
    RANGE = 1

    def __init__(self, pos: tuple[int, int], sprite: str, weapon_type: int, cooldown: float, recoil: float = 0) -> None:
        super(Weapon, self).__init__(pos, sprite)
        self.__type: int = weapon_type
        self.__recoil: float = recoil
        self.__cooldown: float = cooldown  # cooldown duration in seconds
        self.__counter: int = pygame.time.get_ticks()  # time on last action

    def get_recoil(self) -> float:
        return self.__recoil

    def get_cooldown(self) -> float:
        return self.__cooldown

    def get_cooldown_counter(self) -> int:
        return self.__counter

    def update_counter(self) -> None:
        self.__counter = pygame.time.get_ticks()

    def action(self, projectiles: list[Projectile]) -> bool:
        if (pygame.time.get_ticks() - self.__counter) / 1000 > self.__cooldown:

            if self.__type == self.RANGE:
                projectiles.append(Projectile(self.rect.center, (TILE_SCALE / 8, TILE_SCALE / 8),
                                              (255, 255, 0), pygame.mouse.get_pos(), TILE_SCALE / 4))

            elif self.__type == self.MELEE:
                # TODO weapon melee action
                print("melee action")

            self.update_counter()
            return True

        return False
