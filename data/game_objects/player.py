import pygame

from data.constants import TILE_SCALE, SCREEN_HEIGHT
from data.game_objects.collectable import Collectable
from data.game_objects.cursor import Cursor
from data.game_objects.entity import Entity
from data.game_objects.projectile import Projectile
from data.game_objects.tile import Tile


class Player(Entity):
    """
    A player object is an entity which has
    its inputs determined by user inputs.\n
    It has a fixed scale and a proper sprite.\n
    """

    def __init__(self, pos: tuple[int, int]) -> None:
        super(Player, self).__init__(pos, (TILE_SCALE * 2 // 3, TILE_SCALE * 2 // 3),
                                     sprite="resources/sprites/player.png")

    def update_from_inputs(self, inputs: dict[str, bool],
                           neighbor_tiles: list[Tile],
                           neighbor_items: list[Collectable],
                           projectiles: list[Projectile],
                           cursor: Cursor, delta_time: float) -> None:

        # getting player inputs from main loop
        self.left = inputs["left"]
        self.right = inputs["right"]
        self.up = inputs["up"]
        self.down = inputs["down"]
        self.pick = inputs["pick"]
        self.action = inputs["action"]

        self.update(pygame.mouse.get_pos(),
                    neighbor_tiles, neighbor_items, projectiles,
                    delta_time)

        cursor.disable()
        if self.action_possible:
            cursor.enable()

        if self.health <= 0 or self.rect.top > SCREEN_HEIGHT + TILE_SCALE:
            print("GAME OVER")
            pygame.quit()
            quit()
