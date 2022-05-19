import time

import pygame
from numpy import ndarray, array, ndenumerate, around
from numpy.random import choice
from pygame import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN, FULLSCREEN, SCALED
from pygame.display import set_mode, set_caption, flip, get_surface, set_icon
from pygame.event import get
from pygame.mouse import set_visible, get_pos
from pygame.rect import Rect
from pygame.surface import Surface
from pygame.time import Clock

from data.objects.bonus_code import destroy_bonus, update_bonus, display_light
from data.objects.camera_code import update_camera
from data.objects.camera_data import Camera
from data.objects.lava_code import display_lava, update_lava
from data.objects.lava_data import Lava
from data.objects.player_code import update_player, decrease_goo, add_goo_from_bonus
from data.objects.ray_code import update_ray, fire_ray, get_ray_velocity, display_ray
from data.objects.ray_data import Ray
from data.utils.constants import FPS, CURSOR_SPRITE, SCREEN_SIZE, BACKGROUND_SPRITE, \
    TILE_EDGE, WORLD_BOTTOM, WORLD_RIGHT, BACKGROUND_LAVA_SPRITE, GOAL_SPRITES, BONUS_SPRITE, \
    PLAYER_SPRITE, CURSOR_SIZE, ICON, LAVA_TRIGGER_HEIGHT, SHAKE_AMPLITUDE, BACKGROUND_LAVA_DISTANCE, \
    LAVA_WARNING_DURATION, TARGET_FPS
from data.utils.functions import get_screen_grid, rect_inside_screen, animation_frame
from data.utils.generation import generate_world


def main() -> None:
    pygame.init()
    # set_mode(SCREEN_SIZE)
    set_mode(SCREEN_SIZE, FULLSCREEN | SCALED)
    set_icon(ICON)
    set_caption("Goodoo")
    set_visible(False)

    tile_grid, player, goal, bonuses = generate_world()

    ray: Ray = Ray()
    lava: Lava = Lava(WORLD_BOTTOM, Rect(0, WORLD_BOTTOM, WORLD_RIGHT, TILE_EDGE))
    camera: Camera = Camera(array(player.rect.center, dtype=float))

    lava_trigger: bool = False
    shake_counter: float = LAVA_WARNING_DURATION

    timer: float = 0  # incremented every frame by delta time

    screen: Surface = get_surface()

    clock: Clock = Clock()
    last_time: float = time.time()

    while True:
        clock.tick(FPS)

        # delta update using time module because pygame is less precise
        now: float = time.time()
        delta_time = (now - last_time)
        delta: float = delta_time * TARGET_FPS
        last_time = now

        # Events --------------------------------------------------------------

        click: bool = False

        for event in get():

            if event.type == QUIT:
                pygame.quit()
                quit()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    quit()

            elif event.type == MOUSEBUTTONDOWN:
                click = True

        # Model update --------------------------------------------------------

        # camera follows player
        camera = update_camera(camera, array(player.rect.center), delta)

        # lava is triggered when player reached a certain height ...
        if not lava_trigger and player.pos[1] <= LAVA_TRIGGER_HEIGHT * TILE_EDGE:
            lava_trigger = True

        # ... when it occurs, the lava starts moving up and the camera shakes
        if lava_trigger:
            lava = update_lava(lava, delta)
            if shake_counter > 0:
                random_offset: ndarray = choice((-1, 1)) * choice(SHAKE_AMPLITUDE, 2)
                camera = update_camera(camera, player.rect.center + random_offset, delta)
                shake_counter -= delta_time

        # ray starts from the player and aims at mouse position,
        # it's fired on user click and consume player's goo
        ray = update_ray(ray, player, tile_grid, camera, delta)
        if click and ray.power == 0:
            ray = fire_ray(ray)
            player = decrease_goo(player)

        player = update_player(player, get_ray_velocity(ray, player), tile_grid, delta)

        for i, bonus in ndenumerate(bonuses):
            bonuses[i] = update_bonus(bonus, timer)

            # player grabbing bonus destroys it, and gives goo to player
            if player.rect.colliderect(bonus.rect) and bonus.alive:
                bonuses[i] = destroy_bonus(bonus)
                player = add_goo_from_bonus(player)

        # game ends if goal is reached
        if player.rect.colliderect(goal):
            pygame.quit()
            quit()

        # Display -------------------------------------------------------------

        # background
        screen.blit(BACKGROUND_SPRITE, (0, 0))

        if abs(player.pos[1] - lava.y) < BACKGROUND_LAVA_DISTANCE:

            # lava background fades out as player goes away from it and vice versa
            BACKGROUND_LAVA_SPRITE.set_alpha(255 - abs(player.pos[1] - lava.y) / BACKGROUND_LAVA_DISTANCE * 255)
            screen.blit(BACKGROUND_LAVA_SPRITE, (0, 0))

        # TODO add full walls on left and right sides of the tile grid

        # ray
        display_ray(ray, screen, camera)

        # tiles
        visible_tiles: ndarray = get_screen_grid(tile_grid, camera)
        for _, tile in ndenumerate(visible_tiles):
            if tile:
                screen.blit(tile.sprite, around(tile.rect.topleft + camera.offset))

        # goal
        if rect_inside_screen(goal, camera):
            screen.blit(animation_frame(GOAL_SPRITES, timer), around(goal.topleft + camera.offset))

        # player
        screen.blit(PLAYER_SPRITE, around(player.rect.topleft + camera.offset))

        # bonuses
        for bonus in bonuses:
            if rect_inside_screen(bonus.rect, camera) and bonus.alive:
                display_light(screen, array(bonus.rect.center), camera, timer)
                screen.blit(BONUS_SPRITE, around(bonus.rect.topleft + camera.offset))

        # lava
        if rect_inside_screen(lava.rect, camera):
            display_lava(lava, screen, camera, timer)

        # cursor
        screen.blit(CURSOR_SPRITE, array(get_pos()) - CURSOR_SIZE / 2)

        timer += delta_time

        flip()
        # print(int(clock.get_fps()))
