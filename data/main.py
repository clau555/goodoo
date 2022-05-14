import time

import pygame
from numpy import ndarray, array, ndenumerate
from pygame.surface import Surface
from pygame.time import Clock

from data.objects.beam_code import update_beam, fire_beam, get_beam_velocity, display_beam, add_strength
from data.objects.beam_data import Beam
from data.objects.bonus_code import display_bonuses, destroy_bonus, update_bonus
from data.objects.camera_code import update_camera
from data.objects.camera_data import Camera
from data.objects.goal_code import update_goal, display_goal
from data.objects.player_code import update_player, display_player
from data.objects.tile_code import display_tiles
from data.utils.constants import FPS, CURSOR_SPRITE, CURSOR_SIZE, SCREEN_SIZE, BONUS_STRENGTH, BACKGROUND_SPRITE, \
    ANIMATION_SPEED
from data.utils.functions import generate_world, get_screen_grid, rect_inside_screen


def main() -> None:
    pygame.init()
    pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN | pygame.SCALED)
    pygame.display.set_caption("Goodoo")
    pygame.mouse.set_visible(False)

    tile_grid, player, goal, bonuses = generate_world()
    beam: Beam = Beam()
    camera: Camera = Camera()
    animation_counter: int = 0

    clock: Clock = pygame.time.Clock()
    last_time: float = time.time()

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

        camera = update_camera(camera, array(player.rect.center), delta)

        beam = update_beam(beam, player, tile_grid, camera, delta)
        if click and beam.power == 0:
            beam = fire_beam(beam)

        player = update_player(player, get_beam_velocity(beam), tile_grid, delta)

        strength: float = 0
        for i, bonus in ndenumerate(bonuses):
            bonuses[i] = update_bonus(bonus, animation_counter)

            # player grabbing
            if player.rect.colliderect(bonus.rect) and bonus.alive:
                bonuses[i] = destroy_bonus(bonus)
                strength += BONUS_STRENGTH

        beam = add_strength(beam, strength)

        # game ends if goal is reached
        if player.rect.colliderect(goal.rect):
            pygame.quit()
            quit()

        goal = update_goal(goal)

        # -------
        # display
        # -------

        screen: Surface = pygame.display.get_surface()

        screen.blit(BACKGROUND_SPRITE, (0, 0))

        display_beam(beam, screen, camera)

        # only displays tiles visible on screen
        visible_tiles: ndarray = get_screen_grid(tile_grid, camera)
        display_tiles(visible_tiles, screen, camera)

        if rect_inside_screen(goal.rect, camera):
            display_goal(goal, screen, camera)

        display_player(player, screen, camera)

        display_bonuses(bonuses, screen, camera)

        cursor_pos: ndarray = array(pygame.mouse.get_pos()) - CURSOR_SIZE * 0.5
        screen.blit(CURSOR_SPRITE, cursor_pos)

        animation_counter += ANIMATION_SPEED

        pygame.display.flip()
        clock.tick(FPS)
        # print(int(clock.get_fps()))
