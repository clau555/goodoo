from threading import Timer

from numpy import ndarray
from numpy.linalg import norm
from numpy.random import choice

from src.utils.constants import SCREEN_SIZE, LAVA_WARNING_DURATION, CAMERA_SPEED, SHAKE_AMPLITUDE
from src.utils.utils import scale_vec, new_array


class Camera:
    """
    Determine the boundaries and offset to apply to displayed sprites to follow a target during game.
    """

    def __init__(self, target_position: ndarray):
        # world position on which the camera is centered
        self._center: ndarray = target_position
        # world position of the top left corner of the camera
        self._top_left: ndarray = new_array()
        # offset to apply to a sprite position to get its screen position
        self._offset: ndarray = new_array()

        self._shaking_timer: Timer = self._new_timer()

    def _new_timer(self) -> Timer:
        return Timer(LAVA_WARNING_DURATION, self._stop_shaking)

    def _stop_shaking(self):
        self._shaking_timer.cancel()
        self._shaking_timer = self._new_timer()

    @property
    def offset(self):
        return self._offset

    @property
    def top_left(self):
        return self._top_left

    def start_shaking(self) -> None:
        self._shaking_timer.start()

    def update(self, focus_pos: ndarray, delta: float) -> None:
        """
        Updates the camera position based on a focused position.

        :param focus_pos: screen space position on which the camera should be centered
        :param delta: delta between two frames
        """
        focus_pos_: ndarray = focus_pos

        if self._shaking_timer.is_alive():
            random_offset: ndarray = choice((-1, 1)) * choice(SHAKE_AMPLITUDE, 2)
            focus_pos_ += random_offset

        heading: ndarray = focus_pos_ - self._center

        # clamping camera velocity
        velocity: ndarray = heading * CAMERA_SPEED * delta
        if norm(velocity) > norm(heading):
            velocity = scale_vec(velocity, norm(heading))

        center: ndarray = self._center + velocity
        top_left: ndarray = center - SCREEN_SIZE / 2
        offset: ndarray = SCREEN_SIZE / 2 - center

        # camera stops going up when top is reached
        offset[1] = offset[1] if offset[1] <= 0 else 0

        self._center = center
        self._top_left = top_left
        self._offset = offset
