import time
from builtins import int
from random import randrange
from typing import Union

import pygame

from constants import FPS
from displayable import Displayable
from entity import Entity
from level_parser import level_from_image
from player import Player
from projectile import Projectile
from src.cursor import Cursor
from src.object_parser import get_weapons_dict, get_weapon_instance
from tile import Tile
from utils import *
from weapon import Weapon


class Game:
    """
    The game object stores, update, and displays
    every displayable objects of the program.\n
    """

    # time in seconds to pass before an item is created randomly on screen
    ITEM_SPAWN_DELAY: float = 10.

    def __init__(self, level_file_name) -> None:
        self.__player: Player
        self.__tile_map: list[list[Union[Tile, None]]]
        self.__player, self.__tile_map = level_from_image(level_file_name)  # level parsing

        self.__tiles: list[Tile] = self.__get_existing_tiles()
        self.__sky: Displayable = Displayable((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT), sprite="data/sprites/sky.jpg")

        self.__entities: list[Entity] = [self.__player]  # current list of entities in game
        self.__weapons: list[Weapon] = []  # current list of weapons in game

        # an index marked as True indicates an item is already at this emplacement
        self.__item_map: list[list[bool]] = [[False for _ in range(WORLD_HEIGHT)] for _ in range(WORLD_WIDTH)]

        # hardcoded projectile object to test entity/projectile collision
        test_projectile: Projectile = Projectile((0, 500), (TILE_SCALE // 8, TILE_SCALE // 8),
                                                 (255, 255, 255), self.__player.rect.center, TILE_SCALE / 2)
        self.__projectiles: list[Projectile] = [test_projectile]  # current list of projectiles in game

        self.__item_types: dict = get_weapons_dict()
        self.__projectile_types: dict = {}

        self.__cursor: Cursor = Cursor()

        self.__debug: bool = False

        self.__last_item_spawn_time: float = time.time()

        # first two items spawn
        self.__spawn_random_items()
        self.__spawn_random_items()

    @property
    def player(self) -> Player:
        return self.__player

    def toggle_debug(self) -> None:
        self.__debug = not self.__debug

    def __get_existing_tiles(self) -> list[Tile]:
        tiles: list[Tile] = []
        for line in self.__tile_map:
            for tile in line:
                if tile is not None:
                    tiles.append(tile)
        return tiles

    def __neighbor_tiles(self, pos: tuple[int, int]) -> list[Tile]:
        """
        Returns the existing neighbor tiles of a given position on screen.
        The neighbors include at most the 8 surrounding tiles of the position
        and the tile on the position itself.
        :param pos: position on screen
        :return: neighbor tiles
        """
        tile_pos: tuple[int, int] = (int(pos[0] / TILE_SCALE), int(pos[1] / TILE_SCALE))
        tiles: list[Tile] = []
        if 0 <= tile_pos[0] < SCREEN_WIDTH / TILE_SCALE and 0 <= tile_pos[1] < SCREEN_HEIGHT / TILE_SCALE:
            for i in range(tile_pos[0] - 1, tile_pos[0] + 2):
                for j in range(tile_pos[1] - 1, tile_pos[1] + 2):
                    if 0 <= i < len(self.__tile_map) and 0 <= j < len(self.__tile_map[j]) and \
                            self.__tile_map[i][j] is not None:
                        tiles.append(self.__tile_map[i][j])
        return tiles

    def __spawn_random_items(self) -> None:
        indexes: list[tuple[int, int]] = []

        for j in range(WORLD_WIDTH):
            for i in range(WORLD_HEIGHT - 1):
                if self.__tile_map[j][i] is None and \
                        self.__tile_map[j][i + 1] is not None and \
                        not self.__item_map[j][i]:
                    indexes.append((j, i))

        if len(indexes) > 0:
            # getting a random free index placement
            map_pos: tuple[int, int] = indexes[randrange(len(indexes))]
            # and converting it to a screen position
            screen_pos: tuple[int, int] = get_item_placement_from_index(map_pos)

            # loads a random item
            random_key: str = list(self.__item_types.keys())[randrange(len(list(self.__item_types.keys())))]
            item_obj: dict = self.__item_types[random_key]
            item: Weapon = get_weapon_instance(screen_pos, item_obj)
            self.__weapons.append(item)

            # and marking its position as taken
            self.__item_map[map_pos[0]][map_pos[1]] = True

    def update_and_display(self, inputs: dict[str, bool], delta_time: float) -> None:

        # MODEL UPDATE

        # updates user cursor sprite position
        self.__cursor.update()

        # spawns an item randomly when ITEM_SPAWN_DELAY is elapsed
        if (time.time() - self.__last_item_spawn_time) * delta_time > self.ITEM_SPAWN_DELAY:
            self.__spawn_random_items()
            self.__last_item_spawn_time = time.time()

        # player entity updated according to user inputs
        # we pass neighbor tiles only for collisions for better performances
        self.__player.update_from_inputs(inputs, self.__neighbor_tiles(self.__player.rect.center),
                                         self.__weapons, self.__projectiles, self.__cursor, delta_time)

        for collectable in self.__weapons:
            if not collectable.available:
                weapon_pos: tuple[int, int] = get_index_from_screen_position(collectable.rect.center)
                self.__item_map[weapon_pos[0]][weapon_pos[1]] = False
                self.__weapons.pop(self.__weapons.index(collectable))
            else:
                collectable.update(delta_time)

        for projectile in self.__projectiles:
            if not is_inside_screen(projectile.rect) or not projectile.alive:
                self.__projectiles.pop(self.__projectiles.index(projectile))
            else:
                projectile.update(self.__neighbor_tiles(projectile.rect.center), delta_time)

        # DISPLAY UPDATE

        # self.__sky.display()
        pygame.display.get_surface().fill((0, 0, 0))
        for tile in self.__tiles:
            tile.display()
        for entity in self.__entities:
            entity.display()
        for collectable in self.__weapons:
            collectable.display()
        for projectile in self.__projectiles:
            projectile.display()

        self.__cursor.display()

        # DEBUG

        if self.__debug:

            # player collisions
            for tile in self.__neighbor_tiles(self.__player.rect.center):
                pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0),
                                 pygame.Rect((tile.rect.x, tile.rect.y), tile.rect.size))

            # player direction
            start_point = self.__player.rect.center
            end_point = (self.__player.rect.center + self.__player.direction)
            pygame.draw.line(pygame.display.get_surface(), (255, 0, 0), start_point, end_point)

            # fps
            fps_str = str(int(1 / (delta_time / FPS)))
            font = pygame.font.Font(pygame.font.get_default_font(), 32)
            text = font.render(fps_str, False, (255, 0, 0))
            pygame.display.get_surface().blit(text, text.get_rect())
