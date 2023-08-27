import time

from numpy import clip, around, ndarray, array
from pygame import Rect, Surface

from src.utils.constants import WALL_COLOR, BACKGROUND_SPRITE, BACKGROUND_LAVA_SPRITE, LAVA_WARNING_DISTANCE, \
    SCREEN_SIZE, LAVA_WARNING_DURATION


class Background:
    """
    Represents the image displayed as a background during the game.
    The image gets more orange the more the player is close to the lava.
    It also gets orange for a short amount of time when the lava has been triggered.
    """

    def __init__(self):
        self._is_warning: bool = False
        self._warning_counter: float = LAVA_WARNING_DURATION
        self._last_time: float = 0.

    def start_warning(self) -> None:
        self._is_warning = True
        self._last_time = time.time()

    def _update_counter(self) -> None:
        now: float = time.time()
        self._warning_counter -= now - self._last_time
        self._last_time = now

        if self._warning_counter <= 0:
            self._is_warning = False

    def display(
            self,
            player_world_position: ndarray,
            lava_y: int,
            camera_offset: ndarray,
            screen: Surface
    ) -> None:
        """
        Displays background on screen. That includes the background sprite and the left and right side walls.
        Handles lava warning when screen is shaking.

        :param player_world_position: player position in world space
        :param lava_y: lava y coordinate
        :param camera_offset: camera offset from world origin
        :param screen: main screen surface
        """

        portion: Rect = self._portion_rect(camera_offset)
        position: ndarray = self._background_position(camera_offset)

        screen.fill(WALL_COLOR)  # side walls
        screen.blit(BACKGROUND_SPRITE.subsurface(portion), position)  # background sprite

        # lava background is displayed when camera shakes
        if self._is_warning:
            self._update_counter()
            background_portion: Surface = BACKGROUND_LAVA_SPRITE.subsurface(portion)
            alpha: int = int(self._warning_counter / LAVA_WARNING_DURATION * 255)
            background_portion.set_alpha(alpha)
            screen.blit(background_portion, position)

        # lava background fades out as player goes away from it and vice versa
        elif abs(player_world_position[1] - lava_y) < LAVA_WARNING_DISTANCE:
            background_portion: Surface = BACKGROUND_LAVA_SPRITE.subsurface(portion)

            player_distance: int = abs(int(player_world_position[1]) - lava_y)
            alpha: int = int(255 - player_distance / LAVA_WARNING_DISTANCE * 255)
            background_portion.set_alpha(alpha)

            screen.blit(background_portion, position)

    @staticmethod
    def _portion_rect(camera_offset: ndarray) -> Rect:
        """
        Returns current background portion rect in background sprite space.

        :param camera_offset: camera offset from world origin
        :return: background sub rect
        """
        return Rect(
            float(clip(around(camera_offset[0]), 0, None)),
            0,
            SCREEN_SIZE[0] - abs(around(camera_offset[0])),
            float(SCREEN_SIZE[1])
        )

    @staticmethod
    def _background_position(camera_offset: ndarray) -> ndarray:
        """
        Returns current background top left position in screen space.

        :param camera_offset: camera offset from world origin
        :return: background position in screen space
        """
        return array((clip(around(camera_offset[0]), 0, None), 0))
