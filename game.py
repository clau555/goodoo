import pygame
from pygame.event import Event

from config import TILE_SCALE, SCREEN_WIDTH, SCREEN_HEIGHT
from displayable import Displayable
from level_parser import level_from_image
from player import Player
from tile import Tile
from weapon import Weapon


class Game:

    def __init__(self, level_file_name: str = None) -> None:
        self._player: Player
        self._map: list[list[Tile]]
        self._player, self._map = level_from_image(level_file_name)
        self._tiles: list[Tile] = self._get_existing_tiles()
        self._sky: Displayable = Displayable((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT), sprite="assets/sky.jpg")

        self._entities = [self._player]
        self._weapons = [Weapon((int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)), "assets/gun.png")]

        self._debug = False

    def _get_existing_tiles(self) -> list[Tile]:
        tiles: list[Tile] = []
        for line in self._map:
            for tile in line:
                if tile is not None:
                    tiles.append(tile)
        return tiles

    def _neighbor_tiles(self, pos: tuple[int, int]) -> list[Tile]:
        tile_pos = (int(pos[0] / TILE_SCALE), int(pos[1] / TILE_SCALE))
        tiles = []
        if 0 <= tile_pos[0] < SCREEN_WIDTH / TILE_SCALE and 0 <= tile_pos[1] < SCREEN_HEIGHT / TILE_SCALE:
            for i in range(tile_pos[0] - 1, tile_pos[0] + 2):
                for j in range(tile_pos[1] - 1, tile_pos[1] + 2):
                    if 0 <= i < len(self._map):
                        if 0 <= j < len(self._map[j]):
                            if self._map[i][j] is not None:
                                tiles.append(self._map[i][j])
        return tiles

    def update_and_display(self, events: list[Event], delta_time: float) -> None:

        # model update

        # we pass neighbor tiles only for better performance (used for collisions)
        self._player.update_from_inputs(events,
                                        self._neighbor_tiles(self._player.rect.center),
                                        self._weapons,
                                        delta_time)

        # unused items destruction
        for collectable in self._weapons:
            if not collectable.is_active:
                self._weapons.pop(self._weapons.index(collectable))

        # display update

        self._sky.display()

        for tile in self._tiles:
            tile.display()

        for collectable in self._weapons:
            collectable.display()

        for entity in self._entities:
            entity.display()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ASTERISK:
                    self._debug = not self._debug

        if self._debug:
            # player collisions
            for tile in self._neighbor_tiles(self._player.rect.center):
                pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0), pygame.Rect((tile.rect.x, tile.rect.y),
                                                                                        tile.rect.size))

            # player direction
            start_point = self._player.rect.center
            end_point = (self._player.rect.centerx + self._player.direction[0],
                         self._player.rect.centery + self._player.direction[1])
            pygame.draw.line(pygame.display.get_surface(), (255, 0, 0), start_point, end_point)
