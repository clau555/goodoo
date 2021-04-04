from typing import Union

import pygame
from pygame.event import Event
from pygame.rect import Rect

from projectile import Projectile
from constants import TILE_SCALE, SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WORLD_WIDTH, WORLD_HEIGHT
from displayable import Displayable
from entity import Entity
from level_parser import level_from_image
from player import Player
from tile import Tile
from weapon import Weapon


def get_tile_position_from_index(index_pos: tuple[int, int]) -> tuple[int, int]:
    if 0 < index_pos[0] < WORLD_WIDTH and 0 < index_pos[1] < WORLD_HEIGHT:
        return index_pos[0] * TILE_SCALE, index_pos[1] * TILE_SCALE


def get_tile_center_from_index(index_pos: tuple[int, int]) -> tuple[int, int]:
    if 0 < index_pos[0] < WORLD_WIDTH and 0 < index_pos[1] < WORLD_HEIGHT:
        return (index_pos[0] * TILE_SCALE) + TILE_SCALE / 2, \
               (index_pos[1] * TILE_SCALE) + TILE_SCALE / 2


def get_item_placement_from_index(index_pos: tuple[int, int]) -> tuple[int, int]:
    if 0 < index_pos[0] < WORLD_WIDTH and 0 < index_pos[1] < WORLD_HEIGHT:
        return index_pos[0] * TILE_SCALE + TILE_SCALE / 4, \
               index_pos[1] * TILE_SCALE + TILE_SCALE / 4


def is_inside_screen(rect: Rect) -> bool:
    return (0 < rect.left < SCREEN_WIDTH or 0 < rect.right < SCREEN_WIDTH) and \
           (0 < rect.top < SCREEN_HEIGHT or 0 < rect.bottom < SCREEN_HEIGHT)


class Game:

    def __init__(self, level_file_name) -> None:
        self.__player: Player
        self.__map: list[list[Union[Tile, None]]]
        self.__player, self.__map = level_from_image(level_file_name)  # level parsing

        self.__tiles: list[Tile] = self.__get_existing_tiles()
        self.__sky: Displayable = Displayable((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT), sprite="assets/sky.jpg")

        self.__entities: list[Entity] = [self.__player]

        gun: Weapon = Weapon(get_item_placement_from_index((7, 7)), "assets/gun.png", Weapon.RANGE, TILE_SCALE/4)
        saber: Weapon = Weapon(get_item_placement_from_index((9, 7)), "assets/saber.png", Weapon.MELEE)
        sword: Weapon = Weapon(get_item_placement_from_index((11, 7)), "assets/sword.png", Weapon.MELEE)
        self.__weapons: list[Weapon] = [gun, saber, sword]

        self.__projectiles: list[Projectile] = []

        self.__debug: bool = False

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
        tile_pos: tuple[int, int] = (int(pos[0] / TILE_SCALE), int(pos[1] / TILE_SCALE))
        tiles: list[Tile] = []
        if 0 <= tile_pos[0] < SCREEN_WIDTH / TILE_SCALE and 0 <= tile_pos[1] < SCREEN_HEIGHT / TILE_SCALE:
            for i in range(tile_pos[0] - 1, tile_pos[0] + 2):
                for j in range(tile_pos[1] - 1, tile_pos[1] + 2):
                    if 0 <= i < len(self.__map) and 0 <= j < len(self.__map[j]) and self.__map[i][j] is not None:
                        tiles.append(self.__map[i][j])
        return tiles

    def update_and_display(self, events: list[Event], delta_time: float) -> None:

        # MODEL UPDATE

        # we pass neighbor tiles only for better performances (used for collisions)
        self.__player.update_from_inputs(events, self.__neighbor_tiles(self.__player.rect.center),
                                         self.__weapons, self.__projectiles, delta_time)

        for collectable in self.__weapons:
            if not collectable.is_available:
                self.__weapons.pop(self.__weapons.index(collectable))
            else:
                collectable.update(delta_time)

        for projectile in self.__projectiles:
            if not is_inside_screen(projectile.rect) or not projectile.alive:
                self.__projectiles.pop(self.__projectiles.index(projectile))
            else:
                projectile.update(self.__neighbor_tiles(projectile.rect.center), delta_time)

        # DISPLAY UPDATE

        self.__sky.display()
        for tile in self.__tiles:
            tile.display()
        for entity in self.__entities:
            entity.display()
        for collectable in self.__weapons:
            collectable.display()
        for projectile in self.__projectiles:
            projectile.display()

        # DEBUG

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

            for projectile in self.__projectiles:
                start_point = self.__player.get_weapon().rect.center
                end_point = projectile.rect.center
                pygame.draw.line(pygame.display.get_surface(), (255, 0, 0), start_point, end_point)

            # fps
            fps_str = str(int(1 / (delta_time / FPS)))
            font = pygame.font.Font("freesansbold.ttf", 32)
            text = font.render(fps_str, False, (255, 0, 0))
            pygame.display.get_surface().blit(text, text.get_rect())
