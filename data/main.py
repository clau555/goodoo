import time

import pygame
from numpy import ndarray, array, ndenumerate, around, clip
from numpy.random import choice
from pygame import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN, FULLSCREEN, SCALED
from pygame.display import set_mode, set_caption, flip, get_surface, set_icon
from pygame.event import get
from pygame.mouse import set_visible, get_pos
from pygame.rect import Rect
from pygame.surface import Surface
from pygame.time import Clock

from data.objects.bonus_code import destroy_bonus, update_bonus, display_bonus, bonus_inside_screen
from data.objects.camera_code import update_camera
from data.objects.camera_data import Camera
from data.objects.lava_code import display_lava, update_lava, set_lava_triggered
from data.objects.lava_data import Lava
from data.objects.player_code import update_player, decrease_goo, add_goo_from_bonus, display_player
from data.objects.ray_code import update_ray, fire_ray, get_ray_velocity, display_ray
from data.objects.ray_data import Ray
from data.utils.constants import FPS, CURSOR_SPRITE, SCREEN_SIZE, BACKGROUND_SPRITE, TILE_EDGE, CURSOR_SIZE, ICON, \
    LAVA_TRIGGER_HEIGHT, SHAKE_AMPLITUDE, LAVA_WARNING_DURATION, TARGET_FPS, \
    BACKGROUND_LAVA_DISTANCE, BACKGROUND_LAVA_SPRITE, GRID_HEIGHT, WALL_COLOR
from data.utils.functions import get_screen_grid, background_position
from data.utils.generation import generate_world


def main() -> None:
    pygame.init()
    # set_mode(SCREEN_SIZE)
    set_mode(SCREEN_SIZE, FULLSCREEN | SCALED)
    set_icon(ICON)
    set_caption("Goodoo")
    set_visible(False)

    tile_grid, player, bonuses = generate_world()

    ray: Ray = Ray()
    lava: Lava = Lava(GRID_HEIGHT * TILE_EDGE)
    camera: Camera = Camera(array(player.rect.center, dtype=float))

    shake_counter: float = LAVA_WARNING_DURATION

    timer: float = 0  # incremented every frame by delta time

    screen: Surface = get_surface()

    clock: Clock = Clock()
    last_time: float = time.time()

    while True:
        clock.tick(FPS)  # limit fps

        # delta update using time module because pygame is less accurate
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

        # lava is triggered when player reached a certain height
        if not lava.triggered and player.pos[1] <= LAVA_TRIGGER_HEIGHT * TILE_EDGE:
            lava = set_lava_triggered(lava)

        if lava.triggered:
            lava = update_lava(lava, delta)  # lava is moving up
            if shake_counter > 0:
                # camera shakes for a short period of time
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

        # Display -------------------------------------------------------------

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

        # ray
        display_ray(ray, screen, camera)

        # player
        display_player(player, ray, screen, camera, timer)

        # bonuses
        for bonus in bonuses:
            if bonus_inside_screen(bonus, camera) and bonus.alive:
                display_bonus(bonus, screen, camera)

        # lava
        display_lava(lava, screen, camera, timer)

        # cursor
        screen.blit(CURSOR_SPRITE, array(get_pos()) - CURSOR_SIZE / 2)

        timer += delta_time

        flip()
        # print(int(clock.get_fps()))
