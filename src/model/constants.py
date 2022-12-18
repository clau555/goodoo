from pathlib import Path

import pygame.font
from numpy import array, ndarray
from pygame import Surface, Rect
from pygame.constants import K_LEFT, K_RIGHT, K_a, K_d, K_q, K_p
from pygame.font import Font
from pygame.image import load
from pygame.transform import scale

# files paths
DIR_PATH: Path = Path(__file__).parents[2]  # pointing on main directory
RESOURCES_PATH: Path = DIR_PATH / "resources"
SPRITES_PATH: Path = RESOURCES_PATH / "sprites"
PLAYER_PATH: Path = SPRITES_PATH / "player"
LAVA_PATH: Path = SPRITES_PATH / "lava"
AMETHYST_PARTICLE_PATH: Path = SPRITES_PATH / "amethyst_particle"
FOSSILS_PATH: Path = SPRITES_PATH / "fossils"
SPIKES_PATH: Path = SPRITES_PATH / "spikes"

# screen
WINDOW_ICON: Surface = load(RESOURCES_PATH / "icon.png")
WINDOW_TITLE: str = "Goodoo"
SCREEN_SIZE: ndarray = array((384, 216))

# basic colors
BLACK: tuple[int, int, int] = (0, 0, 0)
WHITE: tuple[int, int, int] = (255, 255, 255)

# tiles
TILE_EDGE: int = 12  # tile edge size in pixels
TILE_SIZE: ndarray = array((TILE_EDGE, TILE_EDGE))


def load_tiles_from_sheet() -> list[Surface]:
    """
    Loads the different tile sprites from `tile_sheet.png`.

    :return: list of tile sprites
    """
    tiles: list[Surface] = []
    sheet: Surface = load(SPRITES_PATH / "tile_sheet.png")
    for j in range(0, sheet.get_size()[1], TILE_EDGE):
        for i in range(0, sheet.get_size()[0], TILE_EDGE):
            tiles.append(sheet.subsurface(Rect((i, j), tuple(TILE_SIZE))))
    return tiles


TILE_SPRITES: list[Surface] = load_tiles_from_sheet()

# fossil tiles
FOSSIL_SPRITES: list[Surface] = [load(FOSSILS_PATH / f"fossil_{i}.png") for i in range(1, 7)]
FOSSIL_DENSITY: float = 0.025  # chance for a fossil tile to appear on a full tile
SPIKE_SPRITES: list[Surface] = [load(SPIKES_PATH / f"spike_{i}.png") for i in range(1, 4)]
SPIKE_DENSITY: float = 0.6  # chance for a spike tile to appear on a full tile

# obstacle tiles
OBSTACLE_MAX_DENSITY: float = 0.3  # probability of an obstacle to spawn on a tile at highest map height
AMETHYST_SPRITE: Surface = load(SPRITES_PATH / "amethyst.png")
AMETHYST_DENSITY: float = 0.05  # probability of an obstacle to be an amethyst
MUSHROOM_SPRITE: Surface = load(SPRITES_PATH / "mushroom.png")
MUSHROOM_BUMP_FACTOR: float = -0.9  # factor by which the player's speed is multiplied when hitting a mushroom

# obstacle particles
OBSTACLE_PARTICLE_SPAWN_RATE: float = 0.01  # probability of a particle to spawn on an obstacle in one frame
AMETHYST_PARTICLE_SPRITES: list[Surface] = [
    load(AMETHYST_PARTICLE_PATH / f"amethyst_particle_{i}.png") for i in range(1, 5)
]
MUSHROOM_PARTICLE_LIFESPAN: float = 0.3  # in seconds
MUSHROOM_PARTICLE_VELOCITY_NORM: float = TILE_EDGE / 10
MUSHROOM_PARTICLE_RADIUS: float = 1.5
MUSHROOM_PARTICLE_COLOR: tuple[int, int, int] = (218, 255, 0)
MUSHROOM_PARTICLE_LIGHT_RADIUS: int = 3
MUSHROOM_PARTICLE_LIGHT_TRANSPARENCY: int = 100

MUSHROOM_HEALTH_POINTS: int = 3
MUSHROOM_SHAKE_DURATION: float = 0.3  # time in second a mushroom shakes when hit
MUSHROOM_SHAKE_OFFSET: int = 2

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
PLAYER_SPRITE: Surface = load(PLAYER_PATH / "player_jump.png")
PLAYER_GROUND_SPRITES: list[Surface] = [load(PLAYER_PATH / f"player_ground_{i}.png") for i in range(1, 5)]
PLAYER_COLOR: tuple[int, int, int] = (40, 134, 185)
PLAYER_MAX_V: float = TILE_EDGE - TILE_EDGE / 6
PLAYER_INPUT_V: float = TILE_EDGE / 100

# player particles
PLAYER_PARTICLE_INIT_RADIUS: int = 4
PLAYER_PARTICLE_DECREASE_VELOCITY: float = 0.1
PLAYER_PARTICLE_INIT_VELOCITY: float = 2.5
PLAYER_PARTICLES_SPAWN_NUMBER_COLLISION: int = 3
PLAYER_PARTICLES_SPAWN_NUMBER_DEATH: int = 30

# cursor
CURSOR_SIZE: ndarray = array((6, 6))
CURSOR_SPRITE: Surface = load(SPRITES_PATH / "cursor.png")

# physics
FPS: int = 60
TARGET_FPS: float = 60.
GRAVITY: ndarray = array((0, PLAYER_MAX_V / 100))
ANIMATION_SPEED: float = 0.8  # duration of a sprite frame in seconds

# camera
CAMERA_TARGET_OFFSET: ndarray = array((0, -40))
CAMERA_SPEED: float = 0.08
SHAKE_AMPLITUDE: int = 50

# grapple
GRAPPLE_VECTOR_STEP: float = TILE_EDGE / 3
GRAPPLE_ACCELERATION: float = TILE_EDGE / 50
GRAPPLE_HEAD_VELOCITY: float = TILE_EDGE * 2
GRAPPLE_THICKNESS: int = 3
GRAPPLE_HEAD_RADIUS: int = 4

# lava
LAVA_SPRITES: list[Surface] = [load(LAVA_PATH / f"lava_{i}.png") for i in range(1, 5)]
LAVA_SPEED: float = TILE_EDGE / 10
LAVA_TRIGGER_HEIGHT: int = GRID_HEIGHT - 64
LAVA_WARNING_DURATION: float = 2.25  # number of seconds the screen must shake when triggering lava
LAVA_COLOR: tuple[int, int, int] = (254, 56, 7)

# jauge
JAUGE_SIZE: ndarray = array((2, 128))  # in screen space
JAUGE_RECT: Rect = Rect((0, 0), tuple(JAUGE_SIZE))
JAUGE_RECT.center = SCREEN_SIZE[0] - 10, SCREEN_SIZE[1] // 2
JAUGE_POS: ndarray = array(JAUGE_RECT.topleft)
JAUGE_PLAYER_SIZE: ndarray = array((JAUGE_SIZE[0], 2))

# jauge outline
JAUGE_OUTLINE_SIZE: ndarray = JAUGE_RECT.size + array((2, 2))
JAUGE_OUTLINE_POS: ndarray = JAUGE_POS - array((1, 1))
JAUGE_OUTLINE_SURFACE: Surface = Surface(JAUGE_OUTLINE_SIZE)
JAUGE_OUTLINE_SURFACE.fill(WHITE)
JAUGE_OUTLINE_SURFACE.set_alpha(64)

# background
BACKGROUND_SPRITE: Surface = scale(load(SPRITES_PATH / "background.png"), SCREEN_SIZE)
BACKGROUND_LAVA_SPRITE: Surface = scale(load(SPRITES_PATH / "background_lava.png"), SCREEN_SIZE)
# distance between lava and player at which background starts to change to lava background
LAVA_WARNING_DISTANCE: int = SCREEN_SIZE[1] * 2
WALL_COLOR: tuple[int, int, int] = (50, 37, 29)

# key maps
KEY_MAPS: dict[str, dict[str, list[int]]] = {
    "QWERTY": {
        "left": [K_LEFT, K_a],
        "right": [K_RIGHT, K_d],
        "pause": [K_p],
    },
    "AZERTY": {
        "left": [K_LEFT, K_q],
        "right": [K_RIGHT, K_d],
        "pause": [K_p],
    },
}

GAME_OVER_DURATION: float = 1.8  # number of seconds between player death and game over screen

# font
pygame.font.init()
FONT_TEXT = Font(RESOURCES_PATH / "Retro Gaming.ttf", TILE_EDGE)
FONT_TITLE = Font(RESOURCES_PATH / "Retro Gaming.ttf", TILE_EDGE * 4)

# menu
MENU_TITLE: Surface = FONT_TITLE.render("GOODOO", False, WHITE)
MENU_BUTTONS_LABELS: list[str] = ["START", "QUIT"]
MENU_BUTTON_MARGIN: int = 8
MENU_PARTICLE_SPAWN_RATE: float = 0.05

# pause
GRAY_LAYER: Surface = Surface(SCREEN_SIZE)
GRAY_LAYER.fill(BLACK)
GRAY_LAYER.set_alpha(128)
PAUSE_TEXT: Surface = FONT_TEXT.render("PAUSE", False, WHITE)
