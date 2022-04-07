from dataclasses import dataclass
from pygame import Rect, Vector2, Surface


@dataclass(frozen=True)
class PlayerData:
    rect: Rect
    sprite: Surface
    velocity: Vector2 = Vector2(0)
    on_ground: bool = False
