import pygame

from collectable import Collectable
from constants import TILE_SCALE
from projectile import Projectile


class Weapon(Collectable):
    """
    A weapon is a collectable object that can be stored
    by an entity when it's picked up.\n
    It invokes a projectile towards a specific
    when its action method is triggered.\n
    """

    def __init__(self, pos: tuple[int, int], sprite: str, cooldown: float,
                 recoil: float, auto_grab: bool, projectile_name: str) -> None:
        super(Weapon, self).__init__(pos, sprite, auto_grab)
        self.__recoil: float = recoil
        self.__cooldown: float = cooldown  # cooldown duration in seconds
        self.__projectile_type: str = projectile_name  # projectile the weapon will fire
        self.__counter: int = pygame.time.get_ticks()  # saved time on last action

    @property
    def recoil(self) -> float:
        return self.__recoil

    @property
    def cooldown(self) -> float:
        return self.__cooldown

    @property
    def counter(self) -> int:
        return self.__counter

    def update_counter(self) -> None:
        self.__counter = pygame.time.get_ticks()

    def action(self, projectiles: list[Projectile]) -> bool:
        """
        Triggers the weapon action (for example throwing a projectile)
        if its cooldown is finished.\n
        :param projectiles: current list of projectiles in the game
        :return: true if the action has been successfully done
        """
        if (pygame.time.get_ticks() - self.__counter) / 1000 > self.__cooldown:

            # TODO load from projectiles dict, hard coded projectile for now
            projectiles.append(Projectile(self.rect.center, (TILE_SCALE // 8, TILE_SCALE // 8),
                                          (255, 255, 255), pygame.mouse.get_pos(), TILE_SCALE / 2))
            self.update_counter()
            return True

        return False
