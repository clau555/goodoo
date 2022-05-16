from numpy import array
from pygame import draw
from pygame.rect import Rect
from pygame.surface import Surface

from data.objects.camera_data import Camera
from data.utils.constants import LAVA_INIT_SPEED, WORLD_BOTTOM, GRID_WIDTH, LAVA_SPRITES, TILE_EDGE
from data.utils.functions import animation_frame


def display_lava(lava: Rect, screen: Surface, camera: Camera, counter: float) -> None:
    """
    Displays lava on screen.

    :param lava: lava rectangle
    :param screen: screen surface
    :param camera: camera data
    :param counter: game counter
    """
    lava_: Rect = Rect(lava)
    lava_.topleft += camera.offset
    draw.rect(screen, (254, 56, 7), lava_)

    for i in range(GRID_WIDTH):
        screen.blit(
            animation_frame(LAVA_SPRITES, counter),
            lava_.topleft + array((TILE_EDGE, 0)) * i - array((0, TILE_EDGE / 12))
        )


def update_lava(lava: Rect, delta: float) -> Rect:
    """
    Increases continuously lava's height.

    :param lava: lava rectangle
    :param delta: time elapsed since last frame
    :return: updated lava rectangle
    """
    lava_: Rect = Rect(lava)
    lava_.y -= LAVA_INIT_SPEED * delta
    lava_.height = abs(WORLD_BOTTOM - lava_.y)
    return lava_
