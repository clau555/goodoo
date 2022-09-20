from dataclasses import replace

import pygame
from numpy import ndarray, array
from numpy.linalg import linalg
from pygame.draw import line
from pygame.surface import Surface

from data.objects.camera_data import Camera
from data.objects.player_data import Player
from data.objects.ray_data import Ray
from data.utils.constants import RAY_VECTOR_STEP, RAY_COLOR, RAY_ACCELERATION
from data.utils.functions import scale_vec, world_to_grid, pos_inside_grid


def display_ray(ray: Ray, screen: Surface, camera: Camera) -> None:
    """
    Displays the ray on the screen.

    :param ray: ray data
    :param screen: screen surface
    :param camera: camera data
    """
    line(
        screen,
        RAY_COLOR,
        ray.start + camera.offset,
        ray.end + camera.offset,
        3
    )


def update_ray(ray: Ray, player: Player) -> Ray:
    """
    :param ray: ray data
    :param player: player data
    :return: updated ray data
    """
    return replace(ray, start=array(player.rect.center).astype(float))


def fire(ray: Ray, tile_grid: ndarray, camera: Camera) -> Ray:
    """
    Project the ray starting from the player's position
    to the mouse position and beyond until it collides with a tile.
    :param ray: ray data
    :param tile_grid: world tile grid
    :param camera: camera data
    :return: updated ray data
    """
    end: ndarray = array(ray.start, dtype=float)
    step: ndarray = array(pygame.mouse.get_pos()) - camera.offset - ray.start

    if linalg.norm(step) != 0:

        step = scale_vec(step, RAY_VECTOR_STEP)

        collide: bool = False
        inside_grid: bool = True

        end += step

        # increasing vector until it collides with a tile or goes out of screen
        while not collide and inside_grid:

            idx: ndarray = world_to_grid(end)
            if tile_grid[idx[0], idx[1]]:
                collide = True
            end += step
            inside_grid = pos_inside_grid(end)

    return replace(ray, end=end)


def ray_velocity(ray: Ray) -> ndarray:
    """
    Returns the velocity impulse the ray would give to the player.

    :param ray: ray data
    :return: updated ray data
    """
    v: ndarray = ray.end - ray.start
    if linalg.norm(v) != 0:
        return scale_vec(v, RAY_ACCELERATION)
    return array((0, 0))
