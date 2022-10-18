import sys
import time
from dataclasses import replace
from typing import Sequence, List

import pygame
from numpy import ndarray, array, ndenumerate, around, zeros
from numpy.random import random_sample
from pygame import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN, MOUSEBUTTONUP, FULLSCREEN, SCALED
from pygame.surface import Surface
from pygame.time import Clock

from src.display.background import display_background
from src.display.camera import update_camera, shake_camera
from src.display.jauge import display_jauge
from src.display.obstacle_particles import update_display_amethyst_particles, spawn_obstacle_particle, \
    update_display_mushroom_particles
from src.display.player_particles import spawn_player_particles, update_display_player_particles
from src.game.grapple import update_grapple_start, grapple_acceleration, display_grapple, \
    update_grapple
from src.game.lava import display_lava, update_lava
from src.game.player import update_player, display_player
from src.model.constants import FPS, CURSOR_SPRITE, SCREEN_SIZE, TILE_EDGE, CURSOR_SIZE, WINDOW_ICON, \
    LAVA_WARNING_DURATION, TARGET_FPS, \
    GRID_HEIGHT, CAMERA_TARGET_OFFSET, PLAYER_INPUT_V, OBSTACLE_PARTICLE_SPAWN_RATE, ObstacleType, WINDOW_TITLE
from src.model.dataclasses import Camera, Grapple, Lava, Obstacle, PlayerParticle, Player, PygameEvents, \
    ObstacleParticles
from src.model.generation import generate_world
from src.model.utils import visible_grid, is_pressed


def main(keyboard_layout: str) -> None:
    """
    Handles main game logic, from start to finish.

    :param keyboard_layout: keyboard layout string
    """
    pygame.init()
    pygame.display.set_icon(WINDOW_ICON)
    pygame.display.set_caption(WINDOW_TITLE)
    pygame.display.set_mode(SCREEN_SIZE, FULLSCREEN | SCALED)
    pygame.mouse.set_visible(False)
    pygame.event.set_allowed([QUIT, KEYDOWN, MOUSEBUTTONUP, MOUSEBUTTONDOWN])

    tile_cave, player = generate_world()

    grapple: Grapple = Grapple()
    lava: Lava = Lava(GRID_HEIGHT * TILE_EDGE)
    camera: Camera = Camera(array(player.rect.center))

    obstacle_particles: ObstacleParticles = ObstacleParticles()
    player_particles: List[PlayerParticle] = []

    screen: Surface = pygame.display.get_surface()
    events: PygameEvents = PygameEvents()

    shake_counter: float = LAVA_WARNING_DURATION
    timer: float = 0  # incremented every frame by delta time
    clock: Clock = Clock()
    last_time: float = time.time()

    # main loop
    while True:
        clock.tick(FPS)  # limit fps

        # delta update using time module because pygame is less accurate
        now: float = time.time()
        delta_time: float = (now - last_time)
        delta: float = delta_time * TARGET_FPS
        last_time = now

        # pygame events
        events: PygameEvents = _update_events(events)

        # key actions
        input_velocity: ndarray = _key_input_velocity(player, grapple, keyboard_layout)

        # Data update --------------------------------------------------------------------------------------------------

        # camera follows player
        camera_target: ndarray = player.rect.center + CAMERA_TARGET_OFFSET
        camera = update_camera(camera, camera_target, delta)

        # lava's moving up if triggered
        lava = update_lava(lava, player, delta)

        # camera shakes for a short period of time on lava trigger
        if lava.triggered and shake_counter > 0:
            camera = shake_camera(camera, camera_target, delta)
            shake_counter -= delta_time

        # grapple update handling player click and grapple movement
        grapple = update_grapple(grapple, events, tile_cave, camera, delta)

        # player update
        if events.clicking and grapple.head is grapple.end:  # grapple is attached to a wall
            input_velocity += grapple_acceleration(grapple)
        player = update_player(player, input_velocity, tile_cave, delta)
        grapple = update_grapple_start(grapple, player)  # grapple follows player

        # player particles update
        if player.obstacle_collision:
            player_particles = spawn_player_particles(player_particles, array(player.rect.center))

        if player.rect.centery <= 0:
            pygame.quit()
            sys.exit("You won!")
        elif player.rect.centery >= lava.height:
            pygame.quit()
            sys.exit("You loose!")

        # Display ------------------------------------------------------------------------------------------------------

        # background
        display_background(player, lava, shake_counter, camera, screen)

        # tiles, also spawns obstacle particles
        obstacle_particles = _display_tiles(tile_cave, obstacle_particles, camera, screen)

        # player
        if events.clicking:
            display_grapple(grapple, screen, camera)
        display_player(player, screen, camera, timer)

        # particles
        obstacle_particles = update_display_amethyst_particles(obstacle_particles, screen, camera, delta_time)
        obstacle_particles = update_display_mushroom_particles(obstacle_particles, screen, camera, delta_time)
        player_particles = update_display_player_particles(player_particles, screen, camera, delta)

        # lava
        display_lava(lava, screen, camera, timer)

        # jauge
        display_jauge(player, lava, screen)

        # user cursor
        screen.blit(CURSOR_SPRITE, array(pygame.mouse.get_pos()) - CURSOR_SIZE / 2)

        pygame.display.flip()
        timer += delta_time


def _update_events(events: PygameEvents) -> PygameEvents:
    """
    Update events from pygame event queue.

    :param events: events data
    :return: updated events data
    """
    clicking: bool = events.clicking
    click: bool = False

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

    return replace(events, click=click, clicking=clicking)


def _key_input_velocity(player: Player, grapple: Grapple, keyboard_layout: str) -> ndarray:
    """
    Returns the velocity vector of the player according to the pressed keys.

    :param player: player data
    :param grapple: grapple data
    :param keyboard_layout: keyboard layout string
    :return: velocity vector
    """
    keys: Sequence[bool] = pygame.key.get_pressed()
    input_velocity: ndarray = zeros(2)

    if not player.on_ground and grapple.head is grapple.end:
        if is_pressed("left", keys, keyboard_layout):
            input_velocity += array((-PLAYER_INPUT_V, 0))
        if is_pressed("right", keys, keyboard_layout):
            input_velocity += array((PLAYER_INPUT_V, 0))

    return input_velocity


def _display_tiles(
        tile_cave: ndarray,
        particles: ObstacleParticles,
        camera: Camera,
        screen: Surface
) -> ObstacleParticles:
    """
    Displays the tiles of the tile_cave.
    When an obstacle is on screen, spawns its particles randomly.

    :param tile_cave: tile cave
    :param particles: obstacle particles
    :param camera: camera data
    :param screen: screen surface
    :return: updated particles
    """
    particles_: ObstacleParticles = particles

    visible_tiles: ndarray = visible_grid(tile_cave, camera)
    for _, tile in ndenumerate(visible_tiles):
        if tile:
            screen.blit(tile.sprite, around(tile.rect.topleft + camera.offset))

            # generates random particles on obstacles
            if isinstance(tile, Obstacle) and random_sample() < OBSTACLE_PARTICLE_SPAWN_RATE:

                if tile.type is ObstacleType.MUSHROOM:
                    particles_ = replace(particles_, mushroom=spawn_obstacle_particle(
                        particles_.mushroom,
                        array(tile.rect.center)
                    ))
                elif tile.type is ObstacleType.AMETHYST:
                    particles_ = replace(particles_, amethyst=spawn_obstacle_particle(
                        particles_.amethyst,
                        array(tile.rect.center)
                    ))
                else:
                    raise ValueError("Unknown obstacle type.")

    return particles_
