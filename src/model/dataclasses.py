from dataclasses import dataclass, field
from typing import List

from numpy import ndarray, zeros
from pygame import Rect, Surface

from src.model.constants import ObstacleType, PLAYER_PARTICLE_INIT_RADIUS


@dataclass(frozen=True)
class Tile:
    """
    Rect composing the world map and colliding with player.
    """
    rect: Rect
    sprite: Surface


@dataclass(frozen=True)
class TileMaps:
    """
    Stores the two tile maps of the game.
    The cave map contains tile that will collide with the player.
    The decoration map will be displayed on top of the cave map and will not collide with the player.
    """
    cave: ndarray
    decoration: ndarray


@dataclass(frozen=True)
class Obstacle:
    """
    Tile with special behavior when colliding with player.
    """
    rect: Rect
    sprite: Surface
    type: ObstacleType


@dataclass(frozen=True)
class ObstacleParticle:
    """
    Particles emitted from obstacle tiles.
    Has its position updated every frame until its timer reaches its lifespan.
    """
    pos: ndarray  # in world space
    timer: float = 0


@dataclass(frozen=True)
class ObstacleParticles:
    """
    Contains list of currently displayed obstacle particles.
    """
    amethyst: List[ObstacleParticle] = field(default_factory=lambda: [])
    mushroom: List[ObstacleParticle] = field(default_factory=lambda: [])


@dataclass(frozen=True)
class Player:
    """
    Player is subject to physics and collision with tiles.
    He's influenced by an input velocity.
    """
    pos: ndarray  # in world space
    rect: Rect
    velocity: ndarray = zeros(2)
    on_ground: bool = False
    obstacle_collision: bool = False
    alive: bool = True


@dataclass(frozen=True)
class PlayerParticle:
    """
    Circle with initial velocity subject to gravity.
    Radius diminishes with time until it disappears.
    """
    pos: ndarray  # in world space
    velocity: ndarray
    radius: float = PLAYER_PARTICLE_INIT_RADIUS


@dataclass(frozen=True)
class Grapple:
    """
    Line that starts from the player and goes to a target position.
    A head can be fired from the player position to go to the target position, at a certain speed.
    The grapple provides an output velocity that applied to the player when it reached its target.
    """
    start: ndarray = zeros(2)  # start position of the grapple (=player position) in world space
    end: ndarray = zeros(2)  # end position of the grapple in world space
    head: ndarray = zeros(2)  # actual grapple head position
    head_velocity: ndarray = zeros(2)  # speed of the head
    head_start: ndarray = zeros(2)  # point at which the head is fired


@dataclass(frozen=True)
class Lava:
    """
    Rectangle that rises up through the map when player reaches a certain height.
    The game ends if it reaches the player.
    """
    height: float
    triggered: bool = False


@dataclass(frozen=True)
class Camera:
    """
    Determine the boundaries and offset to apply to displayed sprites to follow a target during game.
    """
    center: ndarray  # world position on which the camera is centered
    top_left: ndarray = zeros(2)  # world position of the top left corner of the camera
    offset: ndarray = zeros(2)  # offset to apply to a sprite position to get its screen position


@dataclass(frozen=True)
class GameEvents:
    """
    Boolean of events that can occurs in the menu screen.
    """
    click: bool = False  # true when left mouse button has just been pressed
    clicking: bool = False  # true when left mouse button is being pressed
    pause: bool = False  # true when pause key has just been pressed


@dataclass(frozen=True)
class MenuEvents:
    """
    Boolean of events that can occurs in the menu screen.
    """
    start: bool = False  # true when any key is down


@dataclass(frozen=True)
class MenuParticle:
    """
    Falling sprite in the background of the menu screen.
    All of its coordinate system is in screen space.
    """
    pos: ndarray
    rect: Rect
    velocity: ndarray
    flipped: bool
