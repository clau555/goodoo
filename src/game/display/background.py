from numpy import clip, around, ndarray, array
from pygame import Rect, Surface

from src.model.constants import WALL_COLOR, BACKGROUND_SPRITE, BACKGROUND_LAVA_SPRITE, LAVA_WARNING_DISTANCE, \
    LAVA_WARNING_DURATION, SCREEN_SIZE
from src.model.dataclasses import Camera, Lava, Player


def display_background(
        player: Player,
        lava: Lava,
        shake_counter: float,
        camera: Camera,
        screen: Surface
) -> None:
    """
    Displays background on screen. That includes the background sprite and the left and right side walls.
    Handles lava warning when screen is shaking.

    :param player: player data
    :param lava: lava data
    :param shake_counter: shake counter
    :param camera: camera data
    :param screen: screen surface
    """
    portion: Rect = _portion_rect(camera)
    pos: ndarray = _background_position(camera)

    screen.fill(WALL_COLOR)  # side walls
    screen.blit(BACKGROUND_SPRITE.subsurface(portion), pos)  # background sprite

    # lava background is displayed when camera shakes
    if lava.triggered and shake_counter > 0:
        background_portion: Surface = BACKGROUND_LAVA_SPRITE.subsurface(portion)
        background_portion.set_alpha(int(shake_counter / LAVA_WARNING_DURATION * 255))
        screen.blit(background_portion, pos)

    # lava background fades out as player goes away from it and vice versa
    elif abs(player.pos[1] - lava.height) < LAVA_WARNING_DISTANCE:
        background_portion: Surface = BACKGROUND_LAVA_SPRITE.subsurface(portion)
        background_portion.set_alpha(255 - abs(player.pos[1] - lava.height) / LAVA_WARNING_DISTANCE * 255)
        screen.blit(background_portion, pos)


def _portion_rect(camera: Camera) -> Rect:
    """
    Returns current background portion rect in background sprite space.

    :param camera: camera data
    :return: background portion rect
    """
    return Rect(
        float(clip(around(camera.offset[0]), 0, None)),
        0,
        SCREEN_SIZE[0] - abs(around(camera.offset[0])),
        SCREEN_SIZE[1]
    )


def _background_position(camera: Camera) -> ndarray:
    """
    Returns current background top left position in screen space.

    :param camera: camera data
    :return: background screen position
    """
    return array((clip(around(camera.offset[0]), 0, None), 0))
