from dataclasses import dataclass, field
from typing import List

from numpy import ndarray, zeros
from pygame import Rect, Surface

from src.model.constants import ObstacleType, PLAYER_PARTICLE_INIT_RADIUS


@dataclass(frozen=True)
class Tile:
    rect: Rect
    sprite: Surface


@dataclass(frozen=True)
class Obstacle:
    rect: Rect
    sprite: Surface
    orientation: ndarray
    type: ObstacleType


@dataclass(frozen=True)
class ObstacleParticle:
    pos: ndarray  # in world space
    timer: float = 0


@dataclass(frozen=True)
class ObstacleParticles:
    amethyst: List[ObstacleParticle] = field(default_factory=lambda: [])
    mushroom: List[ObstacleParticle] = field(default_factory=lambda: [])


@dataclass(frozen=True)
class PlayerParticle:
    pos: ndarray  # in world space
    velocity: ndarray
    radius: float = PLAYER_PARTICLE_INIT_RADIUS


@dataclass(frozen=True)
class Player:
    pos: ndarray  # in world space
    rect: Rect
    velocity: ndarray = zeros(2)
    on_ground: bool = False
    obstacle_collision: bool = False


@dataclass(frozen=True)
class Grapple:
    start: ndarray = zeros(2)  # start position of the grapple (=player position) in world space
    end: ndarray = zeros(2)  # end position of the grapple in world space
    head: ndarray = zeros(2)
    head_velocity: ndarray = zeros(2)
    head_start: ndarray = zeros(2)  # point at which the head is fired


@dataclass(frozen=True)
class Lava:
    height: float
    triggered: bool = False


@dataclass(frozen=True)
class Camera:
    center: ndarray  # world position on which the camera is centered
    heading: ndarray = zeros(2)  # world vector pointing on focus position
    top_left: ndarray = zeros(2)  # world position of the top left corner of the camera
    offset: ndarray = zeros(2)  # offset to apply to a sprite position to get its screen position


@dataclass(frozen=True)
class PygameEvents:
    click: bool = False
    clicking: bool = False
