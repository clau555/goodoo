import time
from typing import List

import pygame
from pygame.math import Vector2
from pygame.surface import Surface
from pygame.time import Clock

from data.beam import update_beam, get_beam_velocity, fire_beam, display_beam, Beam
from data.goal import display_goal, update_goal
from data.utils import FPS, BLACK, CURSOR_SPRITE, CURSOR_SIZE
from data.player import display_player, update_velocity, move_and_collide
from data.utils.screen import SCREEN_SIZE
from data.tile import display_tile, Tile
from data.utils.grid import init_world, get_grid_tiles, get_neighbor_tiles, get_grid_index


def main() -> None:
    pygame.init()
    pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Data Oriented Goodoo")
    pygame.mouse.set_visible(False)

    player, goal, tile_grid = init_world("resources/maps/map1.jpg")
    tiles: List[Tile] = get_grid_tiles(tile_grid)
    beam: Beam = Beam()

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
            beam = fire_beam(beam)
            on_ground = False
        input_v: Vector2 = get_beam_velocity(beam)

        player = update_velocity(player, input_v)
        neighbor_tiles: List[Tile] = get_neighbor_tiles(
            tile_grid, get_grid_index(player.rect)
        )
        player = move_and_collide(player, neighbor_tiles, delta)
        if player.rect.colliderect(goal.rect):
            pygame.quit()
            quit()
        goal = update_goal(goal)

        # -------
        # display
        # -------

        screen: Surface = pygame.display.get_surface()
        screen.fill(BLACK)

        display_goal(goal, screen)
        display_beam(beam, screen)
        display_player(player, screen)
        for tile in tiles:
            display_tile(tile, screen)
        screen.blit(
            CURSOR_SPRITE,
            Vector2(pygame.mouse.get_pos()) - Vector2(CURSOR_SIZE) * 0.5
        )

        pygame.display.flip()
        clock.tick(FPS)
