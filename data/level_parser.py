import sys
from typing import Union

import pygame.image
from pygame.color import Color
from pygame.pixelarray import PixelArray
from pygame.surface import Surface

from data.constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SCALE, WORLD_WIDTH, WORLD_HEIGHT
from data.game_objects.player import Player
from data.game_objects.tile import Tile


def color_comparison(color1: Color, color2: Color, margin: int = 75) -> bool:
    """
    Compares two tuples each representing an rgb color.\n
    Two colors are considered the same if their distances are null more or less a given margin.\n
    :param color1: color of a pixel
    :param color2: color to compare the pixel with
    :param margin: margin of the comparison
    :return: true if the two colors are considered the same
    """
    return color2.r - margin <= color1.r <= color2.r + margin and \
           color2.g - margin <= color1.g <= color2.g + margin and \
           color2.b - margin <= color1.b <= color2.b + margin


def level_from_image(file_name: str) -> tuple[Player, list[list[Union[Tile, None]]]]:
    """
    Creates a 2D array of tiles according to the given image file.\n
    Returns also a player object initialized at its spawn point.\n
    :param file_name: path of the image file
    :return: player and tile 2D array
    """
    im: Surface = pygame.image.load(file_name)
    pixel_array: PixelArray = pygame.PixelArray(im)

    if im.get_width() != WORLD_WIDTH or im.get_height() != WORLD_HEIGHT:
        sys.exit("level map file has a size of {} instead of {}"
                 .format(im.get_size(), (SCREEN_WIDTH // TILE_SCALE, SCREEN_HEIGHT // TILE_SCALE)))

    world: list[list[Tile]] = []
    player: Player = Player((0, 0))
    player_spawn: bool = False

    for i in range(im.get_width()):
        line: list[Union[Tile, None]] = []
        for j in range(im.get_height()):
            current_pixel: Color = im.unmap_rgb(pixel_array[i, j])

            # player spawn point
            if color_comparison(current_pixel, Color((0, 0, 255))) and not player_spawn:
                player.rect.centerx = i * TILE_SCALE + TILE_SCALE // 2
                player.rect.centery = j * TILE_SCALE + TILE_SCALE // 2
                player_spawn = True

            # solid tile
            if color_comparison(current_pixel, Color((255, 255, 255))):
                line.append(Tile((i * TILE_SCALE, j * TILE_SCALE), (60, 60, 60)))
            else:
                line.append(None)

        world.append(line)

    for i in range(len(world)):
        for j in range(len(world[i])):
            # a tile is considered to be "on top" if it doesn't have any tile above it
            if world[i][j] is not None and j > 0 and world[i][j - 1] is None:
                world[i][j].set_top(True)

    if not player_spawn:
        sys.exit("no player spawn point set inside the map")

    return player, world
