from dataclasses import replace

from numpy import ndarray
from numpy.linalg import linalg

from data.constants import CAMERA_SPEED, SCREEN_SIZE
from data.dataclasses import Camera
from data.utils import scale_vec


def update_camera(camera: Camera, focus_pos: ndarray, delta: float) -> Camera:
    """
    Update the camera position based on a focused position.

    :param camera: camera data
    :param focus_pos: screen space position on which the camera should be centered
    :param delta: delta between two frames
    :return: updated camera data
    """
    heading: ndarray = focus_pos - camera.center

    # clamping camera velocity
    v: ndarray = heading * CAMERA_SPEED * delta
    if linalg.norm(v) > linalg.norm(heading):
        v = scale_vec(v, linalg.norm(heading))

    center: ndarray = camera.center + v
    top_left: ndarray = center - SCREEN_SIZE / 2
    offset: ndarray = SCREEN_SIZE / 2 - center

    # camera stops going up when top is reached
    offset[1] = offset[1] if offset[1] <= 0 else 0

    return replace(camera, heading=heading, center=center, top_left=top_left, offset=offset)
