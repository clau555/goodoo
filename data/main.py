import time

import pygame
from numpy import ndarray, array
from pygame.surface import Surface
from pygame.time import Clock

from data.beamCode import update_beam, fire_beam, get_beam_velocity, display_beam
from data.beamData import Beam
from data.goalCode import update_goal, display_goal
from data.playerCode import update_velocity, move_and_collide, display_player
from data.utils.constants import FPS, BLACK, CURSOR_SPRITE, CURSOR_SIZE, SCREEN_SIZE
from data.utils.grid import init_world


def main() -> None:
    pygame.init()
    pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN | pygame.SCALED)
    pygame.display.set_caption("Data Oriented Goodoo")
    pygame.mouse.set_visible(False)

    tile_grid, non_empty_tiles, player, goal = init_world("resources/maps/map1.jpg")
    beam: Beam = Beam()

    clock: Clock = pygame.time.Clock()
    last_time: float = time.time()

    on_ground: bool = False

    click: bool
    input_v: ndarray

    delta: float
    last_time: float

    neighbor_tiles: ndarray
    cursor_pos: ndarray
    screen: Surface

    while True:

        click = False

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

        delta = (time.time() - last_time) * FPS
        last_time = time.time()

        # ------------
        # Model update
        # ------------

        beam = update_beam(beam, player, tile_grid, delta)
        if click and on_ground:
            beam = fire_beam(beam)
            on_ground = False

        input_v = get_beam_velocity(beam)

        # player movement and collisions
        player = update_velocity(player, input_v)
        player = move_and_collide(player, tile_grid, delta)

        # game ends if goal is reached
        if player.rect.colliderect(goal.rect):
            pygame.quit()
            quit()
        goal = update_goal(goal)

        # -------
        # display
        # -------

        screen = pygame.display.get_surface()
        screen.fill(BLACK)

        display_goal(goal, screen)
        display_beam(beam, screen)
        display_player(player, screen)

        for tile in non_empty_tiles:
            screen.blit(tile.sprite, tile.rect.topleft)

        cursor_pos: ndarray = array(pygame.mouse.get_pos()) - CURSOR_SIZE * 0.5
        screen.blit(CURSOR_SPRITE, cursor_pos)

        pygame.display.flip()
        clock.tick(FPS)
        # print(clock.get_fps())
