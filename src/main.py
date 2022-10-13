import sys
import time
from typing import Sequence, List

import pygame
from numpy import ndarray, array, ndenumerate, around, zeros
from numpy.random import random_sample
from pygame import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN, MOUSEBUTTONUP, FULLSCREEN, SCALED
from pygame.surface import Surface
from pygame.time import Clock

from src.display.background import display_background
from src.display.camera import update_camera, shake_camera
from src.display.goo_particles import spawn_goo_particles, update_and_display_goo_particles
from src.display.obstacle_particles import update_and_display_amethyst_particles, spawn_obstacle_particle, \
    update_and_display_mushroom_particles
from src.game.grapple import update_grapple_start, fire, grapple_acceleration, display_grapple, \
    update_grapple_head, reset_grapple_head
from src.game.lava import display_lava, update_lava, trigger_lava, display_lava_counter
from src.game.player import update_player, display_player
from src.model.constants import FPS, CURSOR_SPRITE, SCREEN_SIZE, TILE_EDGE, CURSOR_SIZE, ICON, \
    LAVA_TRIGGER_HEIGHT, LAVA_WARNING_DURATION, TARGET_FPS, \
    GRID_HEIGHT, CAMERA_TARGET_OFFSET, PLAYER_INPUT_V, OBSTACLE_PARTICLE_SPAWN_RATE, ObstacleType
from src.model.dataclasses import Camera, Grapple, Lava, Obstacle, ObstacleParticle, GooParticle
from src.model.generation import generate_world
from src.model.utils import visible_grid, is_pressed


def main(keyboard_layout: str) -> None:
    pygame.init()
    pygame.display.set_icon(ICON)
    pygame.display.set_caption("Goodoo")
    pygame.display.set_mode(SCREEN_SIZE, FULLSCREEN | SCALED)
    pygame.mouse.set_visible(False)
    pygame.event.set_allowed([QUIT, KEYDOWN, MOUSEBUTTONUP, MOUSEBUTTONDOWN])

    tile_cave, player = generate_world()

    grapple: Grapple = Grapple()
    lava: Lava = Lava(GRID_HEIGHT * TILE_EDGE)
    camera: Camera = Camera(array(player.rect.center, dtype=float))

    amethyst_particles: List[ObstacleParticle] = []
    mushroom_particles: List[ObstacleParticle] = []
    goo_particles: List[GooParticle] = []

    shake_counter: float = LAVA_WARNING_DURATION
    timer: float = 0  # incremented every frame by delta time

    screen: Surface = pygame.display.get_surface()

    clock: Clock = Clock()
    last_time: float = time.time()

    clicking: bool = False  # true during mouse button press

    # main loop
    while True:
        clock.tick(FPS)  # limit fps

        # delta update using time module because pygame is less accurate
        now: float = time.time()
        delta_time: float = (now - last_time)
        delta: float = delta_time * TARGET_FPS
        last_time = now

        click: bool = False
        input_velocity: ndarray = zeros(2, dtype=float)

        # Events -------------------------------------------------------------------------------------------------------

        for event in pygame.event.get():

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit("Game ended by player.")

            # mouse click
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                click = True
                clicking = True
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                clicking = False

            elif event.type == QUIT:
                pygame.quit()
                sys.exit()

        # key actions
        keys: Sequence[bool] = pygame.key.get_pressed()
        if not player.on_ground and grapple.head is grapple.end:
            if is_pressed("left", keys, keyboard_layout):
                input_velocity += array((-PLAYER_INPUT_V, 0))
            if is_pressed("right", keys, keyboard_layout):
                input_velocity += array((PLAYER_INPUT_V, 0))

        # Data update --------------------------------------------------------------------------------------------------

        # camera follows player
        camera_target: ndarray = player.rect.center + CAMERA_TARGET_OFFSET
        camera = update_camera(camera, camera_target, delta)

        # lava is triggered when player reached a certain height
        if not lava.triggered and player.pos[1] <= LAVA_TRIGGER_HEIGHT * TILE_EDGE:
            lava = trigger_lava(lava)

        if lava.triggered:
            lava = update_lava(lava, delta)  # lava is moving up

            # camera shakes for a short period of time on lava trigger
            if shake_counter > 0:
                camera = shake_camera(camera, camera_target, delta)
                shake_counter -= delta_time

        # grapple update
        if click:
            grapple = fire(grapple, tile_cave, camera)
        if clicking:
            grapple = update_grapple_head(grapple, delta)
        else:
            grapple = reset_grapple_head(grapple)

        # player update
        if clicking and grapple.head is grapple.end:  # grapple is attached to a wall
            input_velocity += grapple_acceleration(grapple)
        player = update_player(player, input_velocity, tile_cave, delta)
        grapple = update_grapple_start(grapple, player)  # grapple follows player

        # goo particles update
        if player.obstacle_collision:
            goo_particles = spawn_goo_particles(goo_particles, array(player.rect.center, dtype=float))

        # TODO game end
        if player.rect.centery <= 0:
            pygame.quit()
            sys.exit("You won!")
        elif player.rect.centery >= lava.height:
            pygame.quit()
            sys.exit("You loose!")

        # Display ------------------------------------------------------------------------------------------------------

        # background
        display_background(player, lava, shake_counter, camera, screen)

        # tiles
        visible_tiles: ndarray = visible_grid(tile_cave, camera)
        for _, tile in ndenumerate(visible_tiles):
            if tile:
                screen.blit(tile.sprite, around(tile.rect.topleft + camera.offset))

                # generates random particles on obstacles
                if isinstance(tile, Obstacle) and random_sample() < OBSTACLE_PARTICLE_SPAWN_RATE:

                    if tile.type is ObstacleType.MUSHROOM:
                        mushroom_particles = spawn_obstacle_particle(
                            mushroom_particles,
                            array(tile.rect.center, dtype=float)
                        )
                    elif tile.type is ObstacleType.AMETHYST:
                        amethyst_particles = spawn_obstacle_particle(
                            amethyst_particles,
                            array(tile.rect.center, dtype=float)
                        )

        # goo particles
        goo_particles = update_and_display_goo_particles(goo_particles, screen, camera, delta)

        # player
        if clicking:
            display_grapple(grapple, screen, camera)
        display_player(player, screen, camera, timer)

        # obstacles particles
        amethyst_particles = update_and_display_amethyst_particles(amethyst_particles, screen, camera, delta_time)
        mushroom_particles = update_and_display_mushroom_particles(mushroom_particles, screen, camera, delta_time)

        # lava
        display_lava(lava, screen, camera, timer)
        display_lava_counter(lava, player, screen)

        # user cursor
        screen.blit(CURSOR_SPRITE, array(pygame.mouse.get_pos()) - CURSOR_SIZE / 2)

        pygame.display.flip()
        timer += delta_time
