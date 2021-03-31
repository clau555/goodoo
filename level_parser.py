import sys

from PIL import Image

from config import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SCALE
from player import Player
from tile import Tile


def level_from_image(file_name: str) -> tuple[Player, list[list[Tile]]]:
    im: Image = Image.open(file_name).convert('RGB')

    if im.size[0] != SCREEN_WIDTH / TILE_SCALE and im.size[1] != SCREEN_HEIGHT / TILE_SCALE:
        sys.exit("level map file is at size {} instead of {}"
                 .format(im.size, (SCREEN_WIDTH / TILE_SCALE, SCREEN_HEIGHT / TILE_SCALE)))

    comparison_margin = 5
    pixel_comparison_margin = (comparison_margin, comparison_margin, comparison_margin)

    world: list[list[Tile]] = []
    for i in range(im.size[0]):
        line: list[Tile] = []
        for j in range(im.size[1]):
            pixel_is_dark = pixel_comparison_margin[0] > im.getpixel((i, j))[0] and \
                            pixel_comparison_margin[1] > im.getpixel((i, j))[1] and \
                            pixel_comparison_margin[2] > im.getpixel((i, j))[2]
            if not pixel_is_dark:
                line.append(Tile((i * TILE_SCALE, j * TILE_SCALE)))
            else:
                line.append(None)
        world.append(line)

    player = Player((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    return player, world
