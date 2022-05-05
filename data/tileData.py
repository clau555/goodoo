from dataclasses import dataclass

from pygame import Rect, Surface


@dataclass(frozen=True)
class Tile:
    rect: Rect
    sprite: Surface
