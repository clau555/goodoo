import pygame

from config import TILE_SCALE
from entity import Entity
from tile import Tile


class Player(Entity):

    def __init__(self, pos: tuple[int, int]) -> None:
        super(Player, self).__init__(pos, (int(TILE_SCALE / 2), int(TILE_SCALE / 2)), "assets/player.png")

    def move_from_input(self, neighbor_tiles: list[Tile], delta_time: float) -> None:
        self.left = False
        self.right = False
        self.up = False
        self.down = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_q] and not keys[pygame.K_d]:
            self.left = True
        elif keys[pygame.K_d] and not keys[pygame.K_q]:
            self.right = True

        if keys[pygame.K_z]:
            self.up = True

        self.update_pos(neighbor_tiles, delta_time)
