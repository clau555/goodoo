import time

import pygame
from numpy import ndarray, array, ndenumerate
from pygame import FULLSCREEN, SCALED, QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN
from pygame.display import set_mode, set_caption, flip, get_surface
from pygame.event import get
from pygame.mouse import set_visible, get_pos
from pygame.rect import Rect
from pygame.surface import Surface
from pygame.time import Clock

from data.objects.beam_code import update_beam, fire_beam, get_beam_velocity, display_beam, add_strength
from data.objects.beam_data import Beam
from data.objects.bonus_code import destroy_bonus, update_bonus
from data.objects.camera_code import update_camera
from data.objects.camera_data import Camera
from data.objects.lava_code import display_lava, update_lava
from data.objects.player_code import update_player
from data.utils.constants import FPS, CURSOR_SPRITE, CURSOR_SIZE, SCREEN_SIZE, BONUS_STRENGTH, BACKGROUND_SPRITE, \
    ANIMATION_SPEED, TILE_EDGE, WORLD_BOTTOM, WORLD_RIGHT, BACKGROUND_LAVA_SPRITE, GOAL_SPRITES, BONUS_SPRITE, \
    PLAYER_SPRITE
from data.utils.functions import get_screen_grid, rect_inside_screen, animation_frame
from data.utils.generation import generate_world


def main() -> None:
    pygame.init()
    set_mode(SCREEN_SIZE, FULLSCREEN | SCALED)
    set_caption("Goodoo")
    set_visible(False)

    tile_grid, player, goal, bonuses = generate_world()

    beam: Beam = Beam()
    lava: Rect = Rect(0, WORLD_BOTTOM, WORLD_RIGHT, TILE_EDGE)
    camera: Camera = Camera()

    counter: float = 0  # incremented every frame

    screen: Surface = get_surface()

    clock: Clock = Clock()
    last_time: float = time.time()

    while True:

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

        delta: float = (time.time() - last_time) * FPS
        last_time = time.time()

        camera = update_camera(camera, array(player.rect.center), delta)

        lava = update_lava(lava, delta)

        beam = update_beam(beam, player, tile_grid, camera, delta)
        if click and beam.power == 0:
            beam = fire_beam(beam)

        player = update_player(player, get_beam_velocity(beam), tile_grid, delta)

        strength: float = 0
        for i, bonus in ndenumerate(bonuses):
            bonuses[i] = update_bonus(bonus, counter)

            # player grabbing bonus
            if player.rect.colliderect(bonus.rect) and bonus.alive:
                bonuses[i] = destroy_bonus(bonus)
                strength += BONUS_STRENGTH

        # increasing beam impulse velocity
        beam = add_strength(beam, strength)

        # game ends if goal is reached
        if player.rect.colliderect(goal):
            pygame.quit()
            quit()

        # Display -------------------------------------------------------------

        # background
        if abs(player.rect.y - lava.y) > SCREEN_SIZE[1] * 1.5:
            screen.blit(BACKGROUND_SPRITE, (0, 0))
        else:
            # TODO add fading
            screen.blit(BACKGROUND_LAVA_SPRITE, (0, 0))

        # TODO add full walls on left and right sides of the tile grid

        # beam
        display_beam(beam, screen, camera)

        # tiles
        visible_tiles: ndarray = get_screen_grid(tile_grid, camera)
        for _, tile in ndenumerate(visible_tiles):
            if tile:
                screen.blit(tile.sprite, tile.rect.topleft + camera.offset)

        # goal
        if rect_inside_screen(goal, camera):
            screen.blit(animation_frame(GOAL_SPRITES, counter), goal.topleft + camera.offset)

        # player
        screen.blit(PLAYER_SPRITE, player.rect.topleft + camera.offset)

        # bonuses
        for bonus in bonuses:
            if rect_inside_screen(bonus.rect, camera) and bonus.alive:
                screen.blit(BONUS_SPRITE, bonus.rect.topleft + camera.offset)

        # lava
        if rect_inside_screen(lava, camera):
            display_lava(lava, screen, camera, counter)

        # cursor
        screen.blit(CURSOR_SPRITE, array(get_pos()) - CURSOR_SIZE * 0.5)

        counter += ANIMATION_SPEED * delta

        flip()
        clock.tick(FPS)
        # print(int(clock.get_fps()))
