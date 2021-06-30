import pygame

from data.constants import TILE_SCALE, SCREEN_HEIGHT
from data.game_objects.collectable import Collectable
from data.game_objects.entity import Entity
from data.game_objects.projectile import Projectile
from data.game_objects.tile import Tile


class Enemy(Entity):

    def __init__(self, pos: tuple[int, int]) -> None:
        super(Enemy, self).__init__(pos, (TILE_SCALE * 2 // 3, TILE_SCALE * 2 // 3),
                                    sprite="resources/sprites/enemy.png")

    def update_from_ai(self, neighbor_tiles: list[Tile], neighbor_items: list[Collectable],
                       projectiles: list[Projectile], delta_time: float) -> None:

        # TODO

        self.update((0, 0),
                    neighbor_tiles, neighbor_items, projectiles,
                    None, delta_time)

        if self.health <= 0 or self.rect.top > SCREEN_HEIGHT + TILE_SCALE:
            print("VICTORY")
            pygame.quit()
            quit()
