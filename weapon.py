import pygame

from collectable import Collectable
from config import TILE_SCALE
from projectile import Projectile


class Weapon(Collectable):
    """
    A weapon is a collectable object that can be stored
    by an entity when it's picked up.\n
    It invokes a projectile towards a specific
    when its action method is triggered.
    """

    def __init__(self, pos: tuple[int, int], sprite: str, cooldown: float, recoil: float = 0) -> None:
        super(Weapon, self).__init__(pos, sprite)
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

            projectiles.append(Projectile(self.rect.center, (TILE_SCALE // 8, TILE_SCALE // 8),
                                          (255, 255, 255), pygame.mouse.get_pos(), TILE_SCALE / 2))

            self.update_counter()
            return True

        return False
