import sys
import time
from dataclasses import replace
from typing import Sequence, List

import pygame
from numpy import ndarray, array, ndenumerate, around, zeros
from numpy.random import random_sample
from pygame import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame.surface import Surface
from pygame.time import Clock

from src.game.display.background import display_background
from src.game.display.camera import update_camera, shake_camera
from src.game.display.jauge import display_jauge
from src.game.display.obstacle_particles import update_display_amethyst_particles, spawn_obstacle_particle, \
    update_display_mushroom_particles
from src.game.display.player_particles import spawn_player_particles, update_display_player_particles
from src.game.gameplay.grapple import update_grapple_start, grapple_acceleration, display_grapple, \
    update_grapple
from src.game.gameplay.lava import display_lava, update_lava
from src.game.gameplay.player import update_player, display_player
from src.generation.generation import generate_world
from src.model.constants import FPS, CURSOR_SPRITE, TILE_EDGE, CURSOR_SIZE, LAVA_WARNING_DURATION, TARGET_FPS, \
    GRID_HEIGHT, CAMERA_TARGET_OFFSET, PLAYER_INPUT_V, OBSTACLE_PARTICLE_SPAWN_RATE, ObstacleType, \
    PLAYER_PARTICLES_SPAWN_NUMBER_COLLISION, PLAYER_PARTICLES_SPAWN_NUMBER_DEATH, GAME_OVER_DURATION, KEY_MAPS, \
    GRAY_LAYER, PAUSE_TEXT, SCREEN_SIZE
from src.model.dataclasses import Camera, Grapple, Lava, Obstacle, PlayerParticle, Player, GameEvents, \
    ObstacleParticles, TileMaps
from src.model.utils import visible_grid, is_pressed


def game(keyboard_layout: str) -> None:
    """
    Handles main game logic, from start to finish.

    :param keyboard_layout: keyboard layout string
    """
    tile_maps, player = generate_world()

    grapple: Grapple = Grapple()
    lava: Lava = Lava(GRID_HEIGHT * TILE_EDGE)
    camera: Camera = Camera(array(player.rect.center))

    obstacle_particles: ObstacleParticles = ObstacleParticles()
    player_particles: List[PlayerParticle] = []

    screen: Surface = pygame.display.get_surface()
    events: GameEvents = GameEvents()

    clock: Clock = Clock()
    last_time: float = time.time()
    timer: float = 0  # incremented every frame by delta time

    shake_counter: float = LAVA_WARNING_DURATION
    over_counter: float = GAME_OVER_DURATION

    over: bool = False

    # main loop
    while not over:
        clock.tick(FPS)  # limit fps

        # pygame events
        events: GameEvents = _update_events(events, keyboard_layout)

        # pause loop
        if events.pause:
            last_time = _pause(keyboard_layout, screen)

        # delta update using time module because pygame is less accurate
        now: float = time.time()
        delta_time: float = (now - last_time)
        delta: float = delta_time * TARGET_FPS
        last_time = now

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

        player_was_alive: bool = player.alive
        if player.alive:
            # grapple update handling player click and grapple movement
            grapple = update_grapple(grapple, events, tile_maps.cave, camera, delta)

            # player update
            if events.clicking and grapple.head is grapple.end:  # grapple is attached to a wall
                input_velocity += grapple_acceleration(grapple)
            player = update_player(player, input_velocity, tile_maps.cave, delta)
            grapple = update_grapple_start(grapple, player)  # grapple follows player

            # lava collision
            if player.rect.centery >= lava.height:
                player = replace(player, alive=False)

        # player particles update
        if player.obstacle_collision:
            player_particles = spawn_player_particles(
                player_particles, array(player.rect.center), PLAYER_PARTICLES_SPAWN_NUMBER_COLLISION
            )

        # game over
        if not player.alive:
            over_counter -= delta_time
            if player_was_alive:
                player_particles = spawn_player_particles(
                    player_particles, array(player.rect.center), PLAYER_PARTICLES_SPAWN_NUMBER_DEATH
                )
        if player.rect.centery <= 0 or over_counter <= 0:
            over = True

        # Display ------------------------------------------------------------------------------------------------------

        # background
        display_background(player, lava, shake_counter, camera, screen)

        # tiles, also spawns obstacle particles
        obstacle_particles = _display_tile_maps(tile_maps, obstacle_particles, camera, screen)

        # player
        if events.clicking and player.alive:
            display_grapple(grapple, screen, camera)
        if player.alive:
            display_player(player, screen, camera, timer)

        # obstacle particles
        obstacle_particles = update_display_amethyst_particles(obstacle_particles, screen, camera, delta_time)
        obstacle_particles = update_display_mushroom_particles(obstacle_particles, screen, camera, delta_time)

        # lava
        display_lava(lava, screen, camera, timer)

        # player particles
        player_particles = update_display_player_particles(player_particles, screen, camera, delta)

        # jauge
        if player.alive:
            display_jauge(player, lava, screen)

        # user cursor
        screen.blit(CURSOR_SPRITE, array(pygame.mouse.get_pos()) - CURSOR_SIZE / 2)

        pygame.display.flip()
        timer += delta_time


def _update_events(events: GameEvents, keyboard_layout: str) -> GameEvents:
    """
    Update events from pygame event queue inside game screen.

    :param events: events data
    :return: updated events data
    """
    clicking: bool = events.clicking
    click: bool = False
    pause: bool = False

    for event in pygame.event.get():

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit("Game ended by user.")
            elif event.key in KEY_MAPS[keyboard_layout]["pause"]:
                pause = True

        # mouse click
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            click = True
            clicking = True
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            clicking = False

        elif event.type == QUIT:
            pygame.quit()
            sys.exit()

    return replace(events, click=click, clicking=clicking, pause=pause)


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


def _display_tile_maps(
        tile_maps: TileMaps,
        particles: ObstacleParticles,
        camera: Camera,
        screen: Surface
) -> ObstacleParticles:
    """
    Displays the tiles of the tile_cave.
    When an obstacle is on screen, spawns its particles randomly.

    :param particles: obstacle particles
    :param camera: camera data
    :param screen: screen surface
    :return: updated particles
    """
    particles_: ObstacleParticles = particles

    visible_cave: ndarray = visible_grid(tile_maps.cave, camera)
    visible_decoration: ndarray = visible_grid(tile_maps.decoration, camera)

    # displaying all tile maps in one loop to reduce process time
    for (i, j), _ in ndenumerate(visible_cave):

        # cave map
        if visible_cave[i, j]:
            screen.blit(
                visible_cave[i, j].sprite,
                around(visible_cave[i, j].rect.topleft + camera.offset)
            )

            # generates random particles on obstacles
            if isinstance(visible_cave[i, j], Obstacle) and random_sample() < OBSTACLE_PARTICLE_SPAWN_RATE:

                if visible_cave[i, j].type is ObstacleType.MUSHROOM:
                    particles_ = replace(particles_, mushroom=spawn_obstacle_particle(
                        particles_.mushroom,
                        array(visible_cave[i, j].rect.center)
                    ))
                elif visible_cave[i, j].type is ObstacleType.AMETHYST:
                    particles_ = replace(particles_, amethyst=spawn_obstacle_particle(
                        particles_.amethyst,
                        array(visible_cave[i, j].rect.center)
                    ))
                else:
                    raise ValueError("Unknown obstacle type.")

        # decoration map
        if visible_decoration[i, j]:
            screen.blit(
                visible_decoration[i, j].sprite,
                around(visible_decoration[i, j].rect.topleft + camera.offset)
            )

    return particles_


def _pause(keyboard_layout: str, screen: Surface) -> float:
    """
    Pauses the game by blocking the main loop.
    Displays a pause screen and waits for the user to press the pause key again.
    Return the time at which the pause ends for delta time calculation.

    :param keyboard_layout: keyboard layout string
    :param screen: screen surface
    :return: time at which the pause ends
    """
    screen.blit(GRAY_LAYER, (0, 0))
    screen.blit(
        PAUSE_TEXT,
        (SCREEN_SIZE[0] / 2 - PAUSE_TEXT.get_width() / 2,
         SCREEN_SIZE[1] / 2 - PAUSE_TEXT.get_height() / 2)
    )
    pygame.display.flip()

    paused: bool = True
    while paused:
        for event in pygame.event.get():

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    _end_program()
                elif event.key in KEY_MAPS[keyboard_layout]["pause"]:
                    paused = False

            elif event.type == QUIT:
                pygame.quit()
                sys.exit()

    return time.time()


def _end_program():
    pygame.quit()
    sys.exit("Game ended by user.")
