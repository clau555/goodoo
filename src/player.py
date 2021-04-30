from typing import Union

import pygame

from constants import TILE_SCALE
from entity import Entity
from projectile import Projectile
from cursor import Cursor
from tile import Tile
from weapon import Weapon


class Player(Entity):
    """
    A player object is an entity which has
    its inputs determined by user inputs.\n
    It has a fixed scale and a proper sprite.\n
    """

    def __init__(self, pos: tuple[int, int]) -> None:
        super(Player, self).__init__(pos, (TILE_SCALE * 2 // 3, TILE_SCALE * 2 // 3),
                                     sprite="data/sprites/player.png")

    def update_from_inputs(self, inputs: dict[str, bool], neighbor_tiles: list[Tile],
                           weapons: list[Weapon], projectiles: list[Projectile],
                           projectile_objects: dict, cursor: Union[Cursor, None], delta_time: float) -> None:
        # getting player inputs from main loop
        self.left = inputs["left"]
        self.right = inputs["right"]
        self.up = inputs["up"]
        self.down = inputs["down"]
        self.pick = inputs["pick"]
        self.action = inputs["action"]

        self.update(pygame.mouse.get_pos(), neighbor_tiles,
                    weapons, projectiles,
                    projectile_objects, cursor, delta_time)

        if self.health <= 0:
            print("GAME OVER")
            pygame.quit()
            quit()
