import time
from typing import List, Tuple, Sequence

import pygame
from pygame.math import Vector2
from pygame.time import Clock

from data.constants import SCREEN_SIZE, FPS, TILE_EDGE, PLAYER_INPUT_VX, PLAYER_MAX_V, PLAYER_INPUT_VY
from data.playerCode import display_player, update_velocity, move_and_collide
from data.tileCode import display_tile
from data.tileData import TileData
from data.world import init_world, get_grid_tiles, get_neighbor_tiles


def main(level_file_name: str) -> None:

    pygame.init()
    pygame.display.set_mode(
        SCREEN_SIZE, pygame.FULLSCREEN | pygame.SCALED | pygame.HWSURFACE | pygame.DOUBLEBUF
    )
    pygame.display.set_caption("Data Oriented Goodoo")
    pygame.mouse.set_visible(False)

    player, tile_grid = init_world(level_file_name)
    tiles: List[TileData] = get_grid_tiles(tile_grid)

    clock: Clock = pygame.time.Clock()
    last_time: float = time.time()

    while True:

        # user inputs
        input_v: Vector2 = Vector2(0, 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_UP and player.on_ground:
                    input_v.y = -PLAYER_INPUT_VY
        keys: Sequence[bool] = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            input_v.x = -PLAYER_INPUT_VX
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            input_v.x = PLAYER_INPUT_VX

        delta: float = (time.time() - last_time) * FPS
        last_time: float = time.time()

        # Model update
        player = update_velocity(player, input_v)
        player_grid_idx: Tuple[int, int] = (
            player.rect.centerx // TILE_EDGE,
            player.rect.centery // TILE_EDGE
        )
        player = move_and_collide(
            player,
            get_neighbor_tiles(tile_grid, player_grid_idx),
            delta
        )

        # display
        pygame.display.get_surface().fill((0, 0, 0))
        for tile in tiles:
            display_tile(tile)
        display_player(player)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main("resources/maps/map1.jpg")
