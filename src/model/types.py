from enum import Enum

from src.model.dataclasses import Mushroom, Amethyst, Tile

CaveTile = Mushroom | Amethyst | Tile | None


class MenuEvent(Enum):
    UP = "up"
    DOWN = "down"
    ENTER = "enter"
