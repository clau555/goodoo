import time
from typing import Sequence, List

import pygame
from numpy import ndarray, array, ndenumerate, around, clip, zeros
from numpy.random import choice
from pygame import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN, MOUSEBUTTONUP, SCALED, FULLSCREEN
from pygame.rect import Rect
from pygame.surface import Surface
from pygame.time import Clock

from data.camera import update_camera
from data.constants import FPS, CURSOR_SPRITE, SCREEN_SIZE, BACKGROUND_SPRITE, TILE_EDGE, CURSOR_SIZE, ICON, \
    LAVA_TRIGGER_HEIGHT, SHAKE_AMPLITUDE, LAVA_WARNING_DURATION, TARGET_FPS, \
    LAVA_WARNING_DISTANCE, BACKGROUND_LAVA_SPRITE, GRID_HEIGHT, WALL_COLOR, CAMERA_TARGET_OFFSET, PLAYER_INPUT_V
from data.dataclasses import Camera, Grapple, Lava, Obstacle, Particle
from data.generation import generate_world
from data.grapple import update_grapple_start, fire, grapple_acceleration, display_grapple, \
    update_grapple_head, reset_grapple_head
from data.lava import display_lava, update_lava, set_lava_triggered, display_lava_counter
from data.particles import update_and_display_particles, spawn_particle
from data.player import update_player, display_player
from data.utils import visible_grid, background_position, is_pressed


def main(keyboard_layout: str) -> None:
    pygame.init()
    pygame.display.set_icon(ICON)
    pygame.display.set_caption("Goodoo")
    pygame.display.set_mode(SCREEN_SIZE, FULLSCREEN | SCALED)
    pygame.mouse.set_visible(False)
    pygame.event.set_allowed([QUIT, KEYDOWN, MOUSEBUTTONUP, MOUSEBUTTONDOWN])

    tile_grid, player = generate_world()

    grapple: Grapple = Grapple()
    lava: Lava = Lava(GRID_HEIGHT * TILE_EDGE)
    camera: Camera = Camera(array(player.rect.center, dtype=float))
    particles: List[Particle] = []

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
                    quit()

            # mouse click
            elif event.type == MOUSEBUTTONDOWN:
                click = True
                clicking = True
            elif event.type == MOUSEBUTTONUP:
                clicking = False

            elif event.type == QUIT:
                pygame.quit()
                quit()

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
            lava = set_lava_triggered(lava)

        if lava.triggered:
            lava = update_lava(lava, delta)  # lava is moving up
            if shake_counter > 0:
                # camera shakes for a short period of time
                random_offset: ndarray = choice((-1, 1)) * choice(SHAKE_AMPLITUDE, 2)
                camera = update_camera(camera, camera_target + random_offset, delta)
                shake_counter -= delta_time

        # grapple update
        if click:
            grapple = fire(grapple, tile_grid, camera)
        if clicking:
            grapple = update_grapple_head(grapple, delta)
        else:
            grapple = reset_grapple_head(grapple)

        # player update
        if clicking and grapple.head is grapple.end:  # grapple is attached to a wall
            input_velocity += grapple_acceleration(grapple)
        player = update_player(player, input_velocity, tile_grid, delta)
        grapple = update_grapple_start(grapple, player)  # grapple follows player

        # TODO game end
        if player.rect.centery <= 0:
            print("You won!")
            exit()
        elif player.rect.centery >= lava.height:
            print("You lost!")
            exit()

        # Display ------------------------------------------------------------------------------------------------------

        screen.fill(WALL_COLOR)

        # getting background visible area
        portion_rect: Rect = Rect(
            clip(around(camera.offset[0]), 0, None),
            0,
            SCREEN_SIZE[0] - abs(around(camera.offset[0])),
            SCREEN_SIZE[1]
        )
        # background display
        screen.blit(BACKGROUND_SPRITE.subsurface(portion_rect), background_position(camera))

        # lava background is displayed when camera shakes
        if lava.triggered and shake_counter > 0:
            background_portion: Surface = BACKGROUND_LAVA_SPRITE.subsurface(portion_rect)
            background_portion.set_alpha(shake_counter / LAVA_WARNING_DURATION * 255)
            screen.blit(background_portion, background_position(camera))

        # lava background fades out as player goes away from it and vice versa
        elif abs(player.pos[1] - lava.height) < LAVA_WARNING_DISTANCE:
            background_portion: Surface = BACKGROUND_LAVA_SPRITE.subsurface(portion_rect)
            background_portion.set_alpha(255 - abs(player.pos[1] - lava.height) / LAVA_WARNING_DISTANCE * 255)
            screen.blit(background_portion, background_position(camera))

        # tiles
        visible_tiles: ndarray = visible_grid(tile_grid, camera)
        for _, tile in ndenumerate(visible_tiles):
            if tile:
                screen.blit(tile.sprite, around(tile.rect.topleft + camera.offset))

                # generates amethyst particles
                if isinstance(tile, Obstacle):
                    particles = spawn_particle(particles, array(tile.rect.center, dtype=float))

        # player
        if clicking:
            display_grapple(grapple, screen, camera)
        display_player(player, screen, camera, timer)

        # particles
        particles = update_and_display_particles(particles, screen, camera, delta_time)

        # lava
        display_lava(lava, screen, camera, timer)
        display_lava_counter(lava, player, screen)

        # user cursor
        screen.blit(CURSOR_SPRITE, array(pygame.mouse.get_pos()) - CURSOR_SIZE / 2)

        pygame.display.flip()
        timer += delta_time
