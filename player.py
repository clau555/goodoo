import pygame
from pygame.event import Event

from config import TILE_SCALE
from entity import Entity
from tile import Tile
from weapon import Weapon


class Player(Entity):

    def __init__(self, pos: tuple[int, int]) -> None:
        super(Player, self).__init__(pos, (int(TILE_SCALE / 2), int(TILE_SCALE / 2)), sprite="assets/player.png")

    def update_from_inputs(self, events: list[Event], neighbor_tiles: list[Tile],
                           weapons: list[Weapon], delta_time: float) -> None:
        self.left: bool = False
        self.right: bool = False
        self.up: bool = False
        self.down: bool = False

        keys = pygame.key.get_pressed()

        if (keys[pygame.K_q] or keys[pygame.K_LEFT]) and not (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            self.left = True
        elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and not (keys[pygame.K_q] or keys[pygame.K_LEFT]):
            self.right = True

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z or event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    self.up = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    if self.get_weapon():
                        self.get_weapon().action()

        self.update(pygame.mouse.get_pos(), neighbor_tiles, weapons, delta_time)
