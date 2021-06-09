import sys
from typing import Union

from PIL import Image

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SCALE, WORLD_WIDTH, WORLD_HEIGHT
from player import Player
from tile import Tile


# TODO use pygame instead of pillow?


def pixel_comparison(pixel: tuple[int, int, int], color: tuple[int, int, int], margin: int = 75) -> bool:
    """
    Compares two tuples each representing an rgb color.\n
    Two colors are considered the same if their distances are null more or less a given margin.\n
    :param pixel: color of a pixel
    :param color: color to compare the pixel with
    :param margin: margin of the comparison
    :return: true if the two colors are considered the same
    """
    return color[0] - margin <= pixel[0] <= color[0] + margin and \
           color[1] - margin <= pixel[1] <= color[1] + margin and \
           color[2] - margin <= pixel[2] <= color[2] + margin


def level_from_image(file_name: str) -> tuple[Player, list[list[Union[Tile, None]]]]:
    """
    Creates a 2D array of tiles according to the given image file.\n
    Returns also a player object initialized at its spawn point.\n
    :param file_name: path of the image file
    :return: player and tile 2D array
    """
    im: Image = Image.open(file_name).convert('RGB')

    if im.size[0] != WORLD_WIDTH or im.size[1] != WORLD_HEIGHT:
        sys.exit("level map file has a size of {} instead of {}"
                 .format(im.size, (SCREEN_WIDTH // TILE_SCALE, SCREEN_HEIGHT // TILE_SCALE)))

    world: list[list[Tile]] = []
    player: Player = Player((0, 0))
    player_spawn: bool = False

    for i in range(im.size[0]):
        line: list[Union[Tile, None]] = []
        for j in range(im.size[1]):
            current_pixel = im.getpixel((i, j))

            # player spawn point
            if pixel_comparison(current_pixel, (0, 0, 255)) and not player_spawn:
                player.rect.centerx = i * TILE_SCALE + TILE_SCALE // 2
                player.rect.centery = j * TILE_SCALE + TILE_SCALE // 2
                player_spawn = True

            # solid tile
            if pixel_comparison(current_pixel, (255, 255, 255)):
                line.append(Tile((i * TILE_SCALE, j * TILE_SCALE), (60, 60, 60)))
            else:
                line.append(None)

        world.append(line)

    for i in range(len(world)):
        for j in range(len(world[i])):
            # a tile is considered to be "on top" if it doesn't have any tile above it
            if world[i][j] is not None and j > 0 and world[i][j - 1] is None:
                world[i][j].set_at_top(True)

    if not player_spawn:
        sys.exit("no player spawn point set inside the map")

    return player, world
