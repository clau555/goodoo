from typing import Tuple, List, Union

from pygame import Vector2


RESOLUTIONS: List[Tuple[int, int]] = [(1920, 1080), (1280, 720), (960, 540)]
SCREEN_SIZE: Tuple[int, int] = RESOLUTIONS[0]
WORLD_SIZE: Tuple[int, int] = 384, 216  # world size in pixels
WORLD_TO_SCREEN: float = SCREEN_SIZE[0] / WORLD_SIZE[0]


def world_to_screen(pos: Union[Tuple[int, int], Vector2]) -> Tuple[int, int]:
    """
    Converts a world position to screen coordinates.

    :param pos: tuple to convert
    :return: screen coordinates
    """
    return int(pos[0] * WORLD_TO_SCREEN), int(pos[1] * WORLD_TO_SCREEN)


def screen_to_world(pos: Union[Tuple[int, int], Vector2]) -> Tuple[int, int]:
    """
    Converts a screen position to world coordinates.

    :param pos: tuple to convert
    :return: world coordinates
    """
    return int(pos[0] / WORLD_TO_SCREEN), int(pos[1] / WORLD_TO_SCREEN)


def is_inside_screen(pos: Vector2) -> bool:
    """
    Checks if a position is inside the screen.

    :param pos: position to check
    :return: True if inside screen, False otherwise
    """
    return 0 <= pos.x < SCREEN_SIZE[0] and 0 <= pos.y < SCREEN_SIZE[1]
