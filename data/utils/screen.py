from numpy import array, ndarray

RESOLUTIONS: ndarray = array(((1920, 1080), (1280, 720), (960, 540)))
SCREEN_SIZE: ndarray = RESOLUTIONS[0]
SCREEN_CENTER: ndarray = SCREEN_SIZE // 2
WORLD_SIZE: ndarray = array((384, 216))  # world size in pixels
WORLD_TO_SCREEN: float = SCREEN_SIZE[0] / WORLD_SIZE[0]  # world to screen ratio


def world_to_screen(pos: ndarray) -> ndarray:
    """
    Converts a world position to screen coordinates.

    :param pos: world position
    :return: screen coordinates
    """
    return array(pos).astype(float) * WORLD_TO_SCREEN


def screen_to_world(pos: ndarray) -> ndarray:
    """
    Converts a screen position to world coordinates.

    :param pos: screen position
    :return: world coordinates
    """
    return array(pos).astype(float) / WORLD_TO_SCREEN


def is_inside_screen(pos: ndarray) -> bool:
    """
    Checks if a position is inside the screen.

    :param pos: screen position to check
    :return: True if inside screen, False otherwise
    """
    return (0 <= pos).all() and (pos < SCREEN_SIZE).all()
