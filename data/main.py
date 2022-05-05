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
from data.utils.utils import init_world, rect_inside_screen


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

    while True:

        # ------
        # Events
        # ------

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

        # ------------
        # Model update
        # ------------

        delta: float = (time.time() - last_time) * FPS
        last_time = time.time()

        # using an alternate variable rather than player.on_ground because
        # it keeps looping to true/false when on ground due to rect collision
        if player.on_ground:
            on_ground = True

        camera_offset: ndarray = -array(player.rect.center) + SCREEN_SIZE / 2

        beam = update_beam(beam, player, tile_grid, camera_offset, delta)
        if click and on_ground:
            beam = fire_beam(beam)
            on_ground = False

        input_v: ndarray = get_beam_velocity(beam)

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

        screen: Surface = pygame.display.get_surface()
        screen.fill(BLACK)

        display_goal(goal, screen, camera_offset)
        display_beam(beam, screen, camera_offset)
        display_player(player, screen, camera_offset)

        for tile in non_empty_tiles:
            if rect_inside_screen(tile.rect, camera_offset):
                screen.blit(tile.sprite, tile.rect.topleft + camera_offset)

        cursor_pos: ndarray = array(pygame.mouse.get_pos()) - CURSOR_SIZE * 0.5
        screen.blit(CURSOR_SPRITE, cursor_pos)

        pygame.display.flip()
        clock.tick(FPS)
        # print(clock.get_fps())
