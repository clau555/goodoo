from dataclasses import dataclass

from numpy import ndarray, array


@dataclass(frozen=True)
class Camera:
    center: ndarray  # world position on which the camera is centered
    heading: ndarray = array((0, 0))  # world vector pointing on focus position
    top_left: ndarray = array((0, 0))  # world position of the top left corner of the camera
    offset: ndarray = array((0, 0))  # offset to apply to a sprite position to get its screen position
