import time
from typing import List

import pygame
from pygame.math import Vector2
from pygame.surface import Surface
from pygame.time import Clock

from data.beamCode import update_beam, get_beam_velocity, fire, display_beam
from data.beamData import BeamData
from data.constants import SCREEN_SIZE, FPS, BLACK, CURSOR_SPRITE, CURSOR_SIZE
from data.playerCode import display_player, update_velocity, move_and_collide, \
    get_grid_index
from data.tileCode import display_tile
from data.tileData import TileData
from data.world import init_world, get_grid_tiles, get_neighbor_tiles


def main() -> None:

    pygame.init()
    pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Data Oriented Goodoo")
    pygame.mouse.set_visible(False)

    player, tile_grid = init_world("resources/maps/map1.jpg")
    tiles: List[TileData] = get_grid_tiles(tile_grid)
    beam: BeamData = BeamData()

    clock: Clock = pygame.time.Clock()
    last_time: float = time.time()

    on_ground: bool = False

    while True:

        click: bool = False

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        # using an alternate variable rather than player.on_ground because
        # it keeps looping to true/false when on ground due to rect collision
        if player.on_ground:
            on_ground = True

        delta: float = (time.time() - last_time) * FPS
        last_time: float = time.time()

        # ------------
        # Model update
        # ------------

        beam = update_beam(beam, player, tiles, delta)
        if click and on_ground:
            beam = fire(beam)
            on_ground = False
        input_v: Vector2 = get_beam_velocity(beam)

        player = update_velocity(player, input_v)
        neighbor_tiles: List[TileData] = get_neighbor_tiles(
            tile_grid, get_grid_index(player)
        )
        player = move_and_collide(player, neighbor_tiles, delta)

        # -------
        # display
        # -------

        screen: Surface = pygame.display.get_surface()
        screen.fill(BLACK)

        for tile in tiles:
            display_tile(tile, screen)
        display_beam(beam, screen)
        display_player(player, screen)
        screen.blit(
            CURSOR_SPRITE,
            Vector2(pygame.mouse.get_pos()) - Vector2(CURSOR_SIZE) * 0.5
        )

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
