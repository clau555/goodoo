from dataclasses import dataclass, field

from numpy import ndarray, zeros
from pygame import Rect, Surface

from src.model.constants import PLAYER_PARTICLE_INIT_RADIUS, MUSHROOM_SHAKE_DURATION, MUSHROOM_HEALTH_POINTS


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
class Mushroom:
    """
    Mushroom obstacle, makes the player bounce on it on collision.
    It needs a hit counter to be destroyed.
    """
    rect: Rect
    sprite: Surface
    health: int = field(default=MUSHROOM_HEALTH_POINTS, compare=False)
    alive: bool = field(default=True, compare=False)
    shake_counter: float = field(default=MUSHROOM_SHAKE_DURATION, compare=False)


@dataclass(frozen=True)
class Amethyst:
    """
    Amethyst obstacle, kills the player on collision.
    """
    rect: Rect
    sprite: Surface


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
    Contains the lists of currently displayed obstacle particles.
    """
    amethyst: list[ObstacleParticle] = field(default_factory=lambda: [])
    mushroom: list[ObstacleParticle] = field(default_factory=lambda: [])


@dataclass(frozen=True)
class Player:
    """
    Player is subject to physics and collision with tiles.
    He's influenced by an input velocity.
    """
    pos: ndarray  # in world space
    rect: Rect
    velocity: ndarray = field(default_factory=lambda: zeros(2))
    on_ground: bool = False
    colliding_mushrooms: list[Mushroom] = field(default_factory=lambda: [])
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
    # start position of the grapple (=player position) in world space
    start: ndarray = field(default_factory=lambda: zeros(2))
    # end position of the grapple in world space
    end: ndarray = field(default_factory=lambda: zeros(2))
    # position at which the head is fired
    head_start: ndarray = field(default_factory=lambda: zeros(2))
    # actual grapple head position
    head: ndarray = field(default_factory=lambda: zeros(2))
    # speed of the head
    head_velocity: ndarray = field(default_factory=lambda: zeros(2))


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
    # world position on which the camera is centered
    center: ndarray
    # world position of the top left corner of the camera
    top_left: ndarray = field(default_factory=lambda: zeros(2))
    # offset to apply to a sprite position to get its screen position
    offset: ndarray = field(default_factory=lambda: zeros(2))


@dataclass(frozen=True)
class GameEvents:
    """
    Boolean of events that can occurs in the menu screen.
    """
    click: bool = False  # true when left mouse button has just been pressed
    clicking: bool = False  # true when left mouse button is being pressed
    pause: bool = False  # true when pause key has just been pressed
    escape: bool = False  # true when escape key has just been pressed


@dataclass(frozen=True)
class MenuParticle:
    """
    Falling player sprite in the background of the menu screen.
    All of its coordinate system is in screen space.
    """
    pos: ndarray
    rect: Rect
    velocity: ndarray
    flipped: bool
