from typing import Union

import pygame
from pygame.event import Event

from config import TILE_SCALE, SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from displayable import Displayable
from level_parser import level_from_image
from player import Player
from tile import Tile
from weapon import Weapon


class Game:

    def __init__(self, level_file_name: str = None) -> None:
        self.__player: Player
        self.__map: list[list[Union[Tile, None]]]
        self.__player, self.__map = level_from_image(level_file_name)
        self.__tiles: list[Tile] = self.__get_existing_tiles()
        self.__sky: Displayable = Displayable((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT), sprite="assets/sky.jpg")

        self.__entities = [self.__player]
        self.__weapons = [Weapon((int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)), "assets/gun.png", Weapon.RANGE)]

        self.__debug = False

    def get_player(self):
        return self.__player

    def __get_existing_tiles(self) -> list[Tile]:
        tiles: list[Tile] = []
        for line in self.__map:
            for tile in line:
                if tile is not None:
                    tiles.append(tile)
        return tiles

    def __neighbor_tiles(self, pos: tuple[int, int]) -> list[Tile]:
        tile_pos = (int(pos[0] / TILE_SCALE), int(pos[1] / TILE_SCALE))
        tiles = []
        if 0 <= tile_pos[0] < SCREEN_WIDTH / TILE_SCALE and 0 <= tile_pos[1] < SCREEN_HEIGHT / TILE_SCALE:
            for i in range(tile_pos[0] - 1, tile_pos[0] + 2):
                for j in range(tile_pos[1] - 1, tile_pos[1] + 2):
                    if 0 <= i < len(self.__map):
                        if 0 <= j < len(self.__map[j]):
                            if self.__map[i][j] is not None:
                                tiles.append(self.__map[i][j])
        return tiles

    def update_and_display(self, events: list[Event], delta_time: float) -> None:

        # model update

        # we pass neighbor tiles only for better performances (used for collisions)
        self.__player.update_from_inputs(events, self.__neighbor_tiles(self.__player.rect.center),
                                         self.__weapons, delta_time)

        # unused items removal
        for collectable in self.__weapons:
            if not collectable.is_available:
                self.__weapons.pop(self.__weapons.index(collectable))

        # display update

        self.__sky.display()
        for tile in self.__tiles:
            tile.display()
        for collectable in self.__weapons:
            collectable.display()
        for entity in self.__entities:
            entity.display()

        # debug

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ASTERISK:
                    self.__debug = not self.__debug

        if self.__debug:

            # player collisions
            for tile in self.__neighbor_tiles(self.__player.rect.center):
                pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0),
                                 pygame.Rect((tile.rect.x, tile.rect.y), tile.rect.size))

            # player direction
            start_point = self.__player.rect.center
            end_point = (self.__player.rect.center + self.__player.get_direction())
            pygame.draw.line(pygame.display.get_surface(), (255, 0, 0), start_point, end_point)

            # fps
            fps_str = str(int(1 / (delta_time / FPS)))
            font = pygame.font.Font("freesansbold.ttf", 32)
            text = font.render(fps_str, False, (255, 0, 0))
            pygame.display.get_surface().blit(text, text.get_rect())
