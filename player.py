import pygame
from entity import Entity
from tile import Tile


class Player(Entity):

    def __init__(self, pos: tuple[int, int]) -> None:
        super(Player, self).__init__(pos, (20, 20), "assets/player.png")

    def move_from_input(self, neighbor_tiles: list[Tile], delta_time: float) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.left = True
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.right = True

        if keys[pygame.K_SPACE]:
            self.up = True

        self.update_pos(neighbor_tiles, delta_time)

        self.left = False
        self.right = False
        self.up = False
        self.down = False
