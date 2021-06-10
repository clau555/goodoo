from typing import Union

import pygame

from src.game_objects.cursor import Cursor
from src.game_objects.entity import Entity
from src.game_objects.projectile import Projectile
from src.game_objects.collectable import Collectable
from src.game_objects.tile import Tile
from src.constants import TILE_SCALE


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
                           items: list[Collectable], projectiles: list[Projectile],
                           cursor: Union[Cursor, None], delta_time: float) -> None:

        # getting player inputs from main loop
        self.left = inputs["left"]
        self.right = inputs["right"]
        self.up = inputs["up"]
        self.down = inputs["down"]
        self.pick = inputs["pick"]
        self.action = inputs["action"]

        self.update(pygame.mouse.get_pos(), neighbor_tiles,
                    items, projectiles,
                    cursor, delta_time)

        if self.health <= 0:
            print("GAME OVER")
            pygame.quit()
            quit()
