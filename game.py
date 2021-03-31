import pygame

from config import TILE_SCALE, SCREEN_WIDTH, SCREEN_HEIGHT
from displayable import Displayable
from level_parser import level_from_image
from player import Player
from tile import Tile


class Game:

    def __init__(self, level_file_name: str = None) -> None:
        self.player: Player
        self.map: list[list[Tile]]
        self.player, self.map = level_from_image(level_file_name)
        self.tiles: list[Tile] = self._get_existing_tiles()
        self.sky: Displayable = Displayable((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT), sprite="assets/sky.jpg")

    def _get_existing_tiles(self) -> list[Tile]:
        tiles: list[Tile] = []
        for line in self.map:
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
                    if 0 <= i < len(self.map):
                        if 0 <= j < len(self.map[j]):
                            if self.map[i][j] is not None:
                                tiles.append(self.map[i][j])
        return tiles

    def update_and_display(self, delta_time: float) -> None:

        # model update
        # we pass neighbor tiles only for better performance (used for collisions)
        self.player.move_from_input(self._neighbor_tiles((int(self.player.rect.x + self.player.rect.width / 2),
                                                          int(self.player.rect.y + self.player.rect.height / 2))),
                                    delta_time)

        # display
        self.sky.display()
        for tile in self.tiles:
            tile.display()
        self.player.display()
