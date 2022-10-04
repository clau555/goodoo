from dataclasses import replace

import pygame
from numpy import ndarray, array, ndenumerate, around
from numpy.linalg import norm
from pygame import Surface
from pygame.rect import Rect
from pygame.transform import flip

from data.constants import GRAVITY, PLAYER_MAX_V, PLAYER_SPRITE, \
    PLAYER_GROUND_SPRITES, AMETHYST_BUMP_FACTOR
from data.dataclasses import Camera, Player, Obstacle
from data.utils import scale_vec, world_to_grid, moore_neighborhood, idx_inside_grid, animation_frame


def display_player(player: Player, screen: Surface, camera: Camera, timer: float) -> None:
    """
    Displays the player on the screen.
    The player is oriented towards the mouse.

    :param player: player data
    :param screen: screen surface
    :param camera: camera data
    :param timer: game timer
    """
    player_screen_pos: ndarray = around(player.rect.topleft + camera.offset)

    # display ground sprite or jumping sprite
    if player.on_ground:
        sprite: Surface = animation_frame(PLAYER_GROUND_SPRITES, timer)
    else:
        sprite: Surface = PLAYER_SPRITE

    # flipping sprites depending on orientation (player always looks at the user mouse)
    if around(player.rect.centerx + camera.offset[0]) - pygame.mouse.get_pos()[0] < 0:
        screen.blit(sprite, player_screen_pos)
    else:
        screen.blit(flip(sprite, True, False), player_screen_pos)


def update_player(player: Player, input_velocity: ndarray, tile_cave: ndarray, delta: float) -> Player:
    """
    Moves the player according to the input velocity then collide with the tiles.
    If any collision occurs, the player is moved to the appropriate position, and its velocity is updated accordingly.

    :param player: player data
    :param input_velocity: velocity inputted by user
    :param tile_cave: world tile grid
    :param delta: delta between two frames
    :return: updated player data
    """

    # velocity update
    v: ndarray = player.velocity + GRAVITY + input_velocity * delta

    # clamp velocity
    if norm(v) > PLAYER_MAX_V:
        v = scale_vec(v, PLAYER_MAX_V)

    # getting neighbor tiles to check collision
    player_idx: ndarray = world_to_grid(array(player.rect.center))
    if not idx_inside_grid(player_idx):
        raise ValueError("Player out of bounds")
    neighbor_tiles: ndarray = moore_neighborhood(tile_cave, player_idx)

    player_pos: ndarray = array(player.pos)
    player_rect: Rect = Rect(player.rect)

    # x movement executes first
    player_pos[0] += v[0]
    player_rect.x = round(player_pos[0])

    # x collision and correction
    for _, tile in ndenumerate(neighbor_tiles):
        if tile and player_rect.colliderect(tile.rect):

            obstacle_impulse: float = 0
            if isinstance(tile, Obstacle):
                if tile.orientation[0]:
                    obstacle_impulse = -v[0] * AMETHYST_BUMP_FACTOR
                else:
                    obstacle_impulse = -v[0] / AMETHYST_BUMP_FACTOR

            if v[0] > 0:
                player_rect.right = tile.rect.left
                player_pos[0] = player_rect.x
                v[0] = obstacle_impulse
                break

            if v[0] < 0:
                player_rect.left = tile.rect.right
                player_pos[0] = player_rect.x
                v[0] = obstacle_impulse
                break

    # y movement executes second
    player_pos[1] += v[1]
    player_rect.y = round(player_pos[1])

    on_ground: bool = False

    # y collisions and correction
    for _, tile in ndenumerate(neighbor_tiles):
        if tile:

            # checking this because colliderect doesn't detect edge perfect collisions
            if player_rect.bottom == tile.rect.top:
                on_ground = True

            if player_rect.colliderect(tile.rect):

                obstacle_impulse: float = 0
                if isinstance(tile, Obstacle):
                    if tile.orientation[1]:
                        obstacle_impulse = -v[1] * AMETHYST_BUMP_FACTOR
                    else:
                        obstacle_impulse = -v[1] / AMETHYST_BUMP_FACTOR

                if v[1] > 0:
                    player_rect.bottom = tile.rect.top
                    player_pos[1] = player_rect.y
                    v = array((v[0], obstacle_impulse)) if obstacle_impulse else array((0, 0))
                    on_ground = True
                    break

                if v[1] < 0:
                    player_rect.top = tile.rect.bottom
                    player_pos[1] = player_rect.y
                    v[1] = obstacle_impulse
                    break

    return replace(
        player,
        pos=player_pos,
        rect=player_rect,
        velocity=v,
        on_ground=on_ground
    )
