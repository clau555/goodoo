from dataclasses import dataclass


@dataclass(frozen=True)
class Lava:
    height: float
    triggered: bool = False
