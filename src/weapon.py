import pygame

from collectable import Collectable
from projectile import Projectile
from src.constants import TILE_SCALE


def get_projectile_instance(pos: tuple[int, int], target_pos: tuple[int, int],
                            projectile_obj: dict) -> Projectile:
    """
    Returns a projectile object instance with the parameters configuration
    stored inside the weapon object dictionary.\n
    :param pos: projectile starting position on screen
    :param target_pos: projectile targeted position on screen
    :param projectile_obj: dictionary storing the instance parameters
    :return: projectile object
    """
    return Projectile(pos, (TILE_SCALE * projectile_obj["size"], TILE_SCALE * projectile_obj["size"]),
                      projectile_obj["color"], target_pos, TILE_SCALE * projectile_obj["speed"])


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

    def action(self, projectiles: list[Projectile], projectile_objects: dict) -> bool:
        """
        Triggers the weapon action (for example throwing a projectile)
        if its cooldown is finished.\n
        :param projectiles: current list of in game projectiles
        :param projectile_objects: list of all projectile instances configurations
        :return: true if the action has been successfully done
        """
        if (pygame.time.get_ticks() - self.__counter) / 1000 > self.__cooldown:
            # FIXME projectile collides with entity when spawned if it's too big
            projectile: Projectile = get_projectile_instance(self.rect.center, pygame.mouse.get_pos(),
                                                             projectile_objects[self.__projectile_type])
            projectiles.append(projectile)
            self.update_counter()
            return True

        return False
