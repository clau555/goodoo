from dataclasses import replace

from numpy import ndarray, array
from numpy.linalg import linalg
from pygame.draw import line
from pygame.mouse import get_pos
from pygame.surface import Surface

from data.objects.camera_data import Camera
from data.objects.player_data import Player
from data.objects.ray_data import Ray
from data.utils.constants import RAY_POWER_DECREASE, RAY_VECTOR_STEP, TILE_EDGE, RAY_MAX_STRENGTH, RAY_MIN_STRENGTH, \
    RAY_COLOR
from data.utils.functions import scale_vec, pos_inside_screen, world_to_grid, pos_inside_grid


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
        int(ray.power * TILE_EDGE / 2)
    )


def update_ray(ray: Ray, player: Player, tile_grid: ndarray, camera: Camera, delta: float) -> Ray:
    """
    Updates the ray, decreasing its power and setting its start and end points.

    :param ray: ray data
    :param player: player data
    :param tile_grid: world tile grid
    :param camera: camera data, used to calculate mouse position in world
    :param delta: delta between two frames
    :return: updated ray data
    """
    start: ndarray = array(player.rect.center).astype(float)
    end: ndarray = array(start)
    step: ndarray = array(get_pos()) - camera.offset - start

    if linalg.norm(step) != 0:

        collide: bool = False
        step = scale_vec(step, RAY_VECTOR_STEP)
        end += step

        # increasing vector until it collides with a tile or goes out of screen
        while not collide and pos_inside_screen(end, camera) and pos_inside_grid(end):

            idx: ndarray = world_to_grid(end)
            if tile_grid[idx[0], idx[1]]:
                collide = True
            end += step

    # decreasing ray power slowly over time
    power: float = ray.power - RAY_POWER_DECREASE * delta
    power = 0 if power < 0 else power  # clamp power to 0

    return replace(ray, start=start, end=end, power=power)


def fire_ray(ray: Ray) -> Ray:
    """
    Fires the ray, setting its power to the maximum.

    :param ray: ray data
    :return: updated ray data
    """
    return replace(ray, power=1)


def get_ray_velocity(ray: Ray, player: Player) -> ndarray:
    """
    Returns the velocity impulse the ray would give to the player, depending on the player's goo quantity.
    Returns a zero vector if the ray has no power left.

    :param ray: ray data
    :param player: player data
    :return: updated ray data
    """
    if ray.power > 0:
        v: ndarray = ray.start - ray.end
        if linalg.norm(v) != 0:
            if player.goo > 0:
                return scale_vec(v, RAY_MAX_STRENGTH)
            else:
                return scale_vec(v, RAY_MIN_STRENGTH)
    return array((0, 0))
