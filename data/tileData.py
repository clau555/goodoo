from dataclasses import dataclass
from pygame import Rect


@dataclass(frozen=True)
class TileData:
    rect: Rect
    top: bool
