import os
import time
from typing import Sequence

import pygame
from numpy import ndarray, array, ndenumerate, around, clip, zeros
from numpy.random import choice
from pygame import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN, MOUSEBUTTONUP, SCALED, HIDDEN, K_q, K_s, K_d, K_z
from pygame.rect import Rect
from pygame.surface import Surface
from pygame.time import Clock

from data.objects.camera_code import update_camera
from data.objects.camera_data import Camera
from data.objects.grapple_code import update_grapple_start, fire, grapple_acceleration, display_ray, \
    update_grapple_head, reset_grapple_head
from data.objects.grapple_data import Grapple
from data.objects.lava_code import display_lava, update_lava, set_lava_triggered
from data.objects.lava_data import Lava
from data.objects.player_code import update_player, display_player
from data.utils.constants import FPS, CURSOR_SPRITE, SCREEN_SIZE, BACKGROUND_SPRITE, TILE_EDGE, CURSOR_SIZE, ICON, \
    LAVA_TRIGGER_HEIGHT, SHAKE_AMPLITUDE, LAVA_WARNING_DURATION, TARGET_FPS, \
    BACKGROUND_LAVA_DISTANCE, BACKGROUND_LAVA_SPRITE, GRID_HEIGHT, WALL_COLOR, CAMERA_TARGET_OFFSET, PLAYER_INPUT_V
from data.utils.functions import get_screen_grid, background_position
from data.utils.generation import generate_world


def main() -> None:
    pygame.init()

    # setting centered window for SDL
    pygame.display.set_mode(SCREEN_SIZE, HIDDEN | SCALED)
    window_size_scaled: ndarray = array(pygame.display.get_window_size())
    pygame.display.quit()
    pygame.display.init()
    info = pygame.display.Info()
    window_pos: ndarray = array((info.current_w, info.current_h)) // 2 - window_size_scaled // 2
    os.environ["SDL_VIDEO_WINDOW_POS"] = f"{window_pos[0]},{window_pos[1]}"

    # initializing window
    pygame.display.set_icon(ICON)
    pygame.display.set_caption("Goodoo")
    pygame.display.set_mode(SCREEN_SIZE, SCALED)
    pygame.mouse.set_visible(False)
    pygame.event.set_allowed([QUIT, KEYDOWN, MOUSEBUTTONUP, MOUSEBUTTONDOWN])

    # TODO fake fullscreen (borderless window)

    tile_grid, player = generate_world()

    grapple: Grapple = Grapple()
    lava: Lava = Lava(GRID_HEIGHT * TILE_EDGE)
    camera: Camera = Camera(array(player.rect.center, dtype=float))

    shake_counter: float = LAVA_WARNING_DURATION
    timer: float = 0  # incremented every frame by delta time

    screen: Surface = pygame.display.get_surface()

    clock: Clock = Clock()
    last_time: float = time.time()

    clicking: bool = False  # true during mouse button press

    while True:
        clock.tick(FPS)  # limit fps

        # delta update using time module because pygame is less accurate
        now: float = time.time()
        delta_time = (now - last_time)
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

            elif event.type == MOUSEBUTTONDOWN:
                click = True
                clicking = True
            elif event.type == MOUSEBUTTONUP:
                clicking = False

            elif event.type == QUIT:
                pygame.quit()
                quit()

        keys: Sequence[bool] = pygame.key.get_pressed()
        if not player.on_ground and grapple.head is grapple.end:
            # TODO handle at least QWERTY
            if keys[K_q]:
                input_velocity += array((-PLAYER_INPUT_V, 0))
            elif keys[K_d]:
                input_velocity += array((PLAYER_INPUT_V, 0))
            elif keys[K_z]:
                input_velocity += array((0, -PLAYER_INPUT_V))
            elif keys[K_s]:
                input_velocity += array((0, PLAYER_INPUT_V))

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

        if click:
            grapple = fire(grapple, tile_grid, camera)
        if clicking:
            grapple = update_grapple_head(grapple)
        else:
            grapple = reset_grapple_head(grapple)

        if clicking and grapple.head is grapple.end:  # grapple is attached to a wall
            input_velocity += grapple_acceleration(grapple)

        player = update_player(player, input_velocity, tile_grid, delta)

        grapple = update_grapple_start(grapple, player)

        if player.rect.centery <= 0:
            print("You won!")
            exit()
        elif player.rect.centery >= lava.height:
            print("You lost!")
            exit()

        # Display ------------------------------------------------------------------------------------------------------

        screen.fill(WALL_COLOR)

        # background visible area
        portion_rect: Rect = Rect(
            clip(around(camera.offset[0]), 0, None),
            0,
            SCREEN_SIZE[0] - abs(around(camera.offset[0])),
            SCREEN_SIZE[1]
        )

        # background display
        screen.blit(BACKGROUND_SPRITE.subsurface(portion_rect), background_position(camera))

        if lava.triggered and shake_counter > 0:
            # lava background is displayed when camera shakes
            background_portion: Surface = BACKGROUND_LAVA_SPRITE.subsurface(portion_rect)
            background_portion.set_alpha(shake_counter / LAVA_WARNING_DURATION * 255)
            screen.blit(background_portion, background_position(camera))

        elif abs(player.pos[1] - lava.height) < BACKGROUND_LAVA_DISTANCE:
            # lava background fades out as player goes away from it and vice versa
            background_portion: Surface = BACKGROUND_LAVA_SPRITE.subsurface(portion_rect)
            background_portion.set_alpha(255 - abs(player.pos[1] - lava.height) / BACKGROUND_LAVA_DISTANCE * 255)
            screen.blit(background_portion, background_position(camera))

        # tiles
        visible_tiles: ndarray = get_screen_grid(tile_grid, camera)
        for _, tile in ndenumerate(visible_tiles):
            if tile:
                screen.blit(tile.sprite, around(tile.rect.topleft + camera.offset))

        # grapple
        if clicking:
            display_ray(grapple, screen, camera)

        # player
        display_player(player, screen, camera, timer)

        # lava
        display_lava(lava, screen, camera, timer)

        # cursor
        screen.blit(CURSOR_SPRITE, array(pygame.mouse.get_pos()) - CURSOR_SIZE / 2)

        timer += delta_time

        pygame.display.flip()
