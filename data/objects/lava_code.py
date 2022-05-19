from dataclasses import replace

from numpy import array, around
from pygame import draw
from pygame.rect import Rect
from pygame.surface import Surface

from data.objects.camera_data import Camera
from data.objects.lava_data import Lava
from data.utils.constants import LAVA_SPEED, WORLD_BOTTOM, GRID_WIDTH, LAVA_SPRITES, TILE_EDGE
from data.utils.functions import animation_frame


def display_lava(lava: Lava, screen: Surface, camera: Camera, timer: float) -> None:
    """
    Displays lava on screen.

    :param lava: lava data
    :param screen: screen surface
    :param camera: camera data
    :param timer: game timer
    """
    rect: Rect = Rect(lava.rect)
    rect.topleft = around(rect.topleft + camera.offset)
    draw.rect(screen, (254, 56, 7), rect)

    for i in range(GRID_WIDTH):
        screen.blit(
            animation_frame(LAVA_SPRITES, timer),
            rect.topleft + array((TILE_EDGE, 0)) * i - array((0, TILE_EDGE / 12))
        )


def update_lava(lava: Lava, delta: float) -> Lava:
    """
    Increases continuously lava's height.

    :param lava: lava data
    :param delta: time elapsed since last frame
    :return: updated lava rectangle
    """
    rect: Rect = Rect(lava.rect)
    y: float = lava.y - LAVA_SPEED * delta

    rect.y = y
    rect.height = abs(WORLD_BOTTOM - rect.y)

    return replace(lava, y=y, rect=rect)
