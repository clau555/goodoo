from pathlib import Path
from typing import List, Tuple

from numpy import array, ndarray
from pygame import Surface, Rect
from pygame.image import load
from pygame.transform import scale

DIR_PATH: Path = Path(__file__).parents[2]  # pointing on main directory
RESOURCES_PATH: Path = DIR_PATH / "resources"
SPRITES_PATH: Path = RESOURCES_PATH / "sprites"
PLAYER_PATH: Path = SPRITES_PATH / "player"
LAVA_PATH: Path = SPRITES_PATH / "lava"

# screen
ICON: Surface = load(RESOURCES_PATH / "icon.png")
SCREEN_SIZE: ndarray = array((384, 216))
SCREEN_RECT: Rect = Rect(0, 0, *SCREEN_SIZE)

# tiles
TILE_EDGE: int = 12  # tile edge size in pixels
TILE_SIZE: ndarray = array((TILE_EDGE, TILE_EDGE))


def load_tiles_from_sheet() -> List[Surface]:
    """
    Loads the different tile sprites from `tile_sheet.png`.

    :return: list of tile sprites
    """
    tiles: List[Surface] = []
    sheet: Surface = load(SPRITES_PATH / "tile_sheet.png")
    for j in range(0, sheet.get_size()[1], TILE_EDGE):
        for i in range(0, sheet.get_size()[0], TILE_EDGE):
            tiles.append(sheet.subsurface(Rect((i, j), tuple(TILE_SIZE))))
    return tiles


TILE_SPRITES: List[Surface] = load_tiles_from_sheet()

# world grid
GRID_SIZE: ndarray = array((32, 512))  # world size in tiles
GRID_WIDTH: int = GRID_SIZE[0]
GRID_HEIGHT: int = GRID_SIZE[1]

# grid generation
NOISE_DENSITY: float = 0.48  # wall density during noise generation
AUTOMATON_ITERATION: int = 4  # number of automaton steps during generation

# screen dimension in terms of tiles
SCREEN_GRID_SIZE: ndarray = array((SCREEN_SIZE[0] // TILE_EDGE, SCREEN_SIZE[1] // TILE_EDGE))

# player
PLAYER_SIZE: ndarray = array((8, 8))
PLAYER_COLOR_SPRITE: Surface = load(PLAYER_PATH / f"player_jump_color.png")
PLAYER_PALE_SPRITE: Surface = load(PLAYER_PATH / f"player_jump_pale.png")
PLAYER_GROUND_COLOR_SPRITES: List[Surface] = [load(PLAYER_PATH / f"player_ground_color_{i}.png") for i in range(1, 5)]
PLAYER_GROUND_PALE_SPRITES: List[Surface] = [load(PLAYER_PATH / f"player_ground_pale_{i}.png") for i in range(1, 5)]
PLAYER_MAX_V: float = TILE_EDGE - TILE_EDGE / 6
PLAYER_MAX_GOO: int = 20

# cursor
CURSOR_SIZE: ndarray = array((6, 6))
CURSOR_SPRITE: Surface = load(SPRITES_PATH / "cursor.png")

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
RAY_COLOR: Tuple[int, int, int] = (255, 255, 255)

# bonus
BONUS_SIZE: ndarray = array((4, 4))
BONUS_SPRITE: Surface = load(SPRITES_PATH / "bonus.png")
BONUS_REPARTITION: int = GRID_HEIGHT // 10  # height space between bonuses
BONUS_VALUE: int = 15
LIGHT_COLOR: Tuple[int, int, int] = (27, 41, 83)
LIGHT_RADIUS: int = BONUS_SIZE[0] * 3
BONUS_ANIMATION_SPEED: float = 0.6  # duration of light pulse and bonus movement in seconds

# lava
LAVA_SPRITES: List[Surface] = [load(LAVA_PATH / f"lava_{i}.png") for i in range(1, 5)]
LAVA_SPEED: float = TILE_EDGE / 10
LAVA_TRIGGER_HEIGHT: int = GRID_HEIGHT - BONUS_REPARTITION - 20
LAVA_WARNING_DURATION: float = 2.25  # number of seconds the screen must shake when triggering lava

# background
BACKGROUND_SPRITE: Surface = scale(load(SPRITES_PATH / "background.png"), SCREEN_SIZE)
BACKGROUND_LAVA_SPRITE: Surface = scale(load(SPRITES_PATH / "background_lava.png"), SCREEN_SIZE)
BACKGROUND_LAVA_DISTANCE: int = SCREEN_SIZE[1] * 2  # distance between lava and player at which background starts to
# change to lava background
WALL_COLOR: Tuple[int, int, int] = (50, 37, 29)
