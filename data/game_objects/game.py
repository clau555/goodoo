import time
from builtins import int
from random import randrange, randint
from typing import Union

import pygame

from data.constants import FPS
from data.dictionaries import WEAPONS_DICT, BONUSES_DICT
from data.game_objects.bonus import Bonus
from data.game_objects.collectable import Collectable
from data.game_objects.cursor import Cursor
from data.game_objects.displayable import Displayable
from data.game_objects.entity import Entity
from data.game_objects.player import Player
from data.game_objects.projectile import Projectile
from data.game_objects.tile import Tile
from data.game_objects.weapon import Weapon
from data.level_parser import level_from_image
from data.utils import *


def get_weapon_instance(weapon_dict: dict, pos: tuple[int, int]) -> Weapon:
    """
    Returns a weapon instance from resources stored inside the weapon dictionary object.\n
    :param weapon_dict: dictionary storing the instance parameters
    :param pos: weapon position on screen
    :return: weapon object
    """
    return Weapon(pos, "resources/sprites/" + weapon_dict["sprite_file"], weapon_dict["cooldown"],
                  TILE_SCALE * weapon_dict["recoil"], weapon_dict["projectile_name"])


def get_bonus_instance(bonus_dict: dict, pos: tuple[int, int]) -> Bonus:
    """
    Returns a bonus instance from resources stored inside the bonus dictionary object.\n
    :param bonus_dict: dictionary storing the instance parameters
    :param pos: weapon position on screen
    :return: bonus object
    """
    return Bonus(pos, "resources/sprites/" + bonus_dict["sprite_file"], bonus_dict["value"])


def get_random_weapon(pos: tuple[int, int]) -> Weapon:
    """
    Returns a random weapon instance chosen inside the global weapons dictionary.\n
    :param pos: screen position at which the weapon should spawn
    :return: weapon instance
    """
    random_key: str = list(WEAPONS_DICT.keys())[randrange(len(list(WEAPONS_DICT.keys())))]
    item_dict: dict = WEAPONS_DICT[random_key]
    return get_weapon_instance(item_dict, pos)


def get_random_bonus(pos: tuple[int, int]) -> Bonus:
    """
    Returns a random bonus instance chosen inside the global bonuses dictionary.\n
    :param pos: screen position at which the bonus should spawn
    :return: bonus instance
    """
    random_key: str = list(BONUSES_DICT.keys())[randrange(len(list(BONUSES_DICT.keys())))]
    item_dict: dict = BONUSES_DICT[random_key]
    return get_bonus_instance(item_dict, pos)


class Game:
    """
    The game object stores, update, and displays
    every displayable objects of the program.\n
    """

    # time in seconds to pass before an item is created randomly on screen
    ITEM_SPAWN_DELAY: float = 10.

    def __init__(self, level_file_name) -> None:
        self.__player: Player  # entity controlled by user
        self.__tile_map: list[list[Union[Tile, None]]]  # 2D array storing solid tiles of the map in their correct index
        self.__player, self.__tile_map = level_from_image(level_file_name)  # level parsing

        self.__tiles: list[Tile] = self.__get_existing_tiles()  # list of all solid tiles in the map
        self.__sky: Displayable = Displayable((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT), sprite="resources/sprites/sky.jpg")

        self.__entities: list[Entity] = [self.__player]     # current list of entities in game
        self.__items: list[Collectable] = []                # current list of items in game

        # an index marked as True indicates an item is already at this emplacement
        self.__item_map: list[list[bool]] = [[False for _ in range(WORLD_HEIGHT)] for _ in range(WORLD_WIDTH)]

        # hardcoded projectile object to test entity/projectile collision
        test_projectile: Projectile = Projectile((0, 500), (TILE_SCALE // 8, TILE_SCALE // 8),
                                                 (255, 255, 255), self.__player.rect.center, TILE_SCALE / 2)
        self.__projectiles: list[Projectile] = [test_projectile]  # current list of projectiles in game

        self.__cursor: Cursor = Cursor()

        self.__debug: bool = False

        self.__last_item_spawn_time: float = time.time()

        # first two items spawn
        self.__spawn_random_item()
        self.__spawn_random_item()

    @property
    def player(self) -> Player:
        return self.__player

    def toggle_debug(self) -> None:
        self.__debug = not self.__debug

    def __get_existing_tiles(self) -> list[Tile]:
        """
        Returns all solid tiles on the map in an array.\n
        :return: existing tiles on the map
        """
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

    def __spawn_random_item(self) -> None:

        # indexes stores all free emplacements coordinates
        indexes: list[tuple[int, int]] = []
        for j in range(WORLD_WIDTH):
            for i in range(WORLD_HEIGHT - 1):
                if self.__tile_map[j][i] is None and \
                        self.__tile_map[j][i + 1] is not None and \
                        not self.__item_map[j][i]:
                    indexes.append((j, i))

        if len(indexes) > 0:
            # getting a random free index placement...
            map_pos: tuple[int, int] = indexes[randrange(len(indexes))]
            # ...and converting it to a position on screen
            screen_pos: tuple[int, int] = get_item_placement_from_index(map_pos)

            # loading a random item (a weapon or a bonus)
            if bool(randint(0, 2)):  # 2 chances out of 3 to be a weapon
                item: Weapon = get_random_weapon(screen_pos)
            else:
                item: Bonus = get_random_bonus(screen_pos)

            # adding the item to the global list to make it spawn...
            self.__items.append(item)
            # ...and marking its position as taken
            self.__item_map[map_pos[0]][map_pos[1]] = True

    def update_and_display(self, inputs: dict[str, bool], delta_time: float) -> None:

        # MODEL UPDATE ##############################################################

        # updates user cursor sprite position
        self.__cursor.update()

        # spawns an item randomly when ITEM_SPAWN_DELAY is elapsed
        if (time.time() - self.__last_item_spawn_time) * delta_time > self.ITEM_SPAWN_DELAY:
            self.__spawn_random_item()
            self.__last_item_spawn_time = time.time()

        # player entity updated according to user inputs
        # we pass neighbor tiles only for collisions for better performances
        # TODO could pass neighbor items only
        self.__player.update_from_inputs(inputs, self.__neighbor_tiles(self.__player.rect.center),
                                         self.__items, self.__projectiles,
                                         self.__cursor, delta_time)

        # items update
        for item in self.__items:
            if not item.available:
                # the item has been picked up, we can delete it from the map
                index: tuple[int, int] = get_index_from_screen_position(item.rect.center)
                self.__item_map[index[0]][index[1]] = False
                self.__items.pop(self.__items.index(item))
            else:
                # idle item
                item.update(delta_time)

        # projectiles update
        for projectile in self.__projectiles:
            # the projectile is destroyed when it collides or if it's outside the screen
            if not is_inside_screen(projectile.rect) or not projectile.alive:
                self.__projectiles.pop(self.__projectiles.index(projectile))
            else:
                projectile.update(self.__neighbor_tiles(projectile.rect.center), delta_time)

        # DISPLAY UPDATE ############################################################

        # self.__sky.display()
        pygame.display.get_surface().fill((0, 0, 0))
        for tile in self.__tiles:
            tile.display()
        for entity in self.__entities:
            entity.display()
        for item in self.__items:
            item.display()
        for projectile in self.__projectiles:
            projectile.display()
        self.__cursor.display()

        # DEBUG #####################################################################

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
