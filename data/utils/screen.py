from typing import Tuple, List

from pygame import Vector2


RESOLUTIONS: List[Tuple[int, int]] = [(1920, 1080), (1280, 720), (960, 540)]
SCREEN_SIZE: Tuple[int, int] = RESOLUTIONS[2]
WORLD_SIZE: Tuple[int, int] = 384, 216  # world size in pixels
PIX_TO_SCREEN: float = SCREEN_SIZE[0] / WORLD_SIZE[0]


def vec_to_screen(pos: Vector2) -> Tuple[int, int]:
    """
    Converts a vector to screen coordinates.

    :param pos: vector to convert
    :return: screen coordinates
    """
    return int(pos.x * PIX_TO_SCREEN), int(pos.y * PIX_TO_SCREEN)


def tuple_to_screen(pos: Tuple[int, int]) -> Tuple[int, int]:
    """
    Converts a tuple to screen coordinates.

    :param pos: tuple to convert
    :return: screen coordinates
    """
    return int(pos[0] * PIX_TO_SCREEN), int(pos[1] * PIX_TO_SCREEN)


def tuple_to_pix(pos: Tuple[int, int]) -> Vector2:
    """
    Converts a tuple to model coordinates.

    :param pos: tuple to convert
    :return: model coordinates
    """
    return Vector2(pos[0] / PIX_TO_SCREEN, pos[1] / PIX_TO_SCREEN)
