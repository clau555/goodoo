from dataclasses import replace

from numpy import ndarray

from data.objects.camera_data import Camera
from data.utils.constants import CAMERA_SPEED, SCREEN_SIZE


def update_camera(camera: Camera, focus_pos: ndarray, delta: float) -> Camera:
    """
    Update the camera position based on a focused position.

    :param camera: camera data
    :param focus_pos: screen space position on which the camera should be centered
    :param delta: delta between two frames
    :return: updated camera data
    """
    heading: ndarray = focus_pos - camera.center
    center: ndarray = camera.center + heading * CAMERA_SPEED * delta
    top_left: ndarray = center - SCREEN_SIZE / 2
    offset: ndarray = SCREEN_SIZE / 2 - center

    # camera stops going up when top is reached
    offset[1] = offset[1] if offset[1] <= 0 else 0

    return replace(camera, heading=heading, center=center, top_left=top_left, offset=offset)
