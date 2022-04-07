from dataclasses import dataclass
from pygame import Vector2


@dataclass(frozen=True)
class BeamData:
    start: Vector2 = Vector2(0)
    end: Vector2 = Vector2(0)
    power: float = 0.0
