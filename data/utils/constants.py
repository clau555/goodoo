from pathlib import Path
from typing import List, Tuple

from numpy import array, ndarray
from pygame import Surface, Rect
from pygame.image import load
from pygame.mask import Mask, from_surface
from pygame.transform import scale

DIR_PATH: Path = Path(__file__).parents[2]  # pointing on main directory
RESOURCES_PATH: Path = DIR_PATH / "resources"
SPRITES_PATH: Path = RESOURCES_PATH / "sprites"

# screen
ICON: Surface = load(RESOURCES_PATH / "icon.png")
SCREEN_SIZE: ndarray = array((384, 216))
SCREEN_RECT: Rect = Rect(0, 0, *SCREEN_SIZE)

# tile
TILE_EDGE: int = 12  # tile edge size in pixels
TILE_SIZE: ndarray = array((TILE_EDGE, TILE_EDGE))
TILE_IMG: Surface = load(SPRITES_PATH / "tile.png")
TILE_SPRITE: Surface = scale(TILE_IMG, TILE_SIZE)

# world grid
GRID_SIZE: ndarray = array((32, 512))  # world size in tiles
GRID_WIDTH: int = GRID_SIZE[0]
GRID_HEIGHT: int = GRID_SIZE[1]
WORLD_RIGHT: int = GRID_WIDTH * TILE_EDGE
WORLD_BOTTOM: int = GRID_HEIGHT * TILE_EDGE

# grid generation
NOISE_DENSITY: float = 0.48  # wall density during noise generation
AUTOMATON_ITERATION: int = 4  # number of automaton steps during generation
PLAYER_SPAWN_HEIGHT: int = GRID_HEIGHT - 3

# screen dimension in terms of tiles
SCREEN_GRID_SIZE: ndarray = array((SCREEN_SIZE[0] // TILE_EDGE, SCREEN_SIZE[1] // TILE_EDGE))

# goal tile
GOAL_SIZE: ndarray = array((10, 10))
GOAL_IMAGES: List[Surface] = [load(SPRITES_PATH / f"goal_{i}.png") for i in range(1, 4)]
GOAL_SPRITES: List[Surface] = list(map(lambda img: scale(img, GOAL_SIZE), GOAL_IMAGES))

# player
PLAYER_SIZE: ndarray = array((8, 8))
PLAYER_IMG: Surface = load(SPRITES_PATH / "player_1.png")  # TODO player animation
PLAYER_SPRITE: Surface = scale(PLAYER_IMG, PLAYER_SIZE)
PLAYER_MAX_V: float = TILE_EDGE - TILE_EDGE / 6
PLAYER_MAX_GOO: int = 40

# cursor
CURSOR_SIZE: ndarray = array((6, 6))
CURSOR_IMG: Surface = load(SPRITES_PATH / "cursor.png")
CURSOR_SPRITE: Surface = scale(CURSOR_IMG, CURSOR_SIZE)

# physics
FPS: int = 60
TARGET_FPS: float = 60.
GRAVITY: ndarray = array((0, PLAYER_MAX_V / 100))
ANIMATION_SPEED: float = 0.8  # duration of a sprite frame in seconds
CAMERA_SPEED: float = 0.08
SHAKE_AMPLITUDE: int = 50

# ray
RAY_POWER_DECREASE: float = 1 / (0.3 * TARGET_FPS)
RAY_VECTOR_STEP: float = TILE_EDGE / 3
RAY_MIN_STRENGTH: float = TILE_EDGE / 10
RAY_MAX_STRENGTH: float = TILE_EDGE / 4

# bonus
BONUS_SIZE: ndarray = array((4, 4))
BONUS_IMG: Surface = load(SPRITES_PATH / "bonus.png")
BONUS_SPRITE: Surface = scale(BONUS_IMG, BONUS_SIZE)
BONUS_REPARTITION: int = GRID_HEIGHT // 10  # height space between bonuses
BONUS_VALUE: int = 15
LIGHT_COLOR: Tuple[int, int, int] = (27, 41, 83)
LIGHT_RADIUS: int = BONUS_SIZE[0] * 3
BONUS_ANIMATION_SPEED: float = 0.6  # duration of light pulse and bonus movement in seconds

# lava
LAVA_IMAGES: List[Surface] = [load(SPRITES_PATH / "lava.png")]  # TODO lava animation
LAVA_SPRITES: List[Surface] = list(map(lambda img: scale(img, TILE_SIZE), LAVA_IMAGES))
LAVA_SPEED: float = TILE_EDGE / 10
LAVA_TRIGGER_HEIGHT: int = GRID_HEIGHT - BONUS_REPARTITION - 10
LAVA_WARNING_DURATION: float = 1.5  # number of seconds the screen must shake when triggering lava

# background
BACKGROUND_SIZE: ndarray = array((192, 108))
BACKGROUND_IMG: Surface = load(SPRITES_PATH / "background.png")
BACKGROUND_SPRITE: Surface = scale(BACKGROUND_IMG, SCREEN_SIZE)
BACKGROUND_LAVA_IMG: Surface = load(SPRITES_PATH / "background_lava.png")
BACKGROUND_LAVA_SPRITE: Surface = scale(BACKGROUND_LAVA_IMG, SCREEN_SIZE)
BACKGROUND_LAVA_DISTANCE: int = SCREEN_SIZE[1] * 2

BACKGROUND_FULL: Surface = Surface(BACKGROUND_SIZE)
BACKGROUND_FULL.fill((50, 37, 29))
BACKGROUND_MASK: Mask = from_surface(BACKGROUND_SPRITE)
GRID_MASK: Mask = from_surface(Surface(GRID_SIZE * TILE_EDGE))
