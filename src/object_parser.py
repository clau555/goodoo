import json
from typing import IO

from src.constants import TILE_SCALE
from src.weapon import Weapon


def get_weapons_dict() -> dict:
    file: IO = open('data/objects.json')
    data: dict = json.load(file)
    file.close()
    return data["weapons"]


def get_weapon_instance(pos: tuple[int, int], weapon_obj: dict) -> Weapon:
    return Weapon(pos, "data/sprites/" + weapon_obj["sprite_file"], weapon_obj["cooldown"],
                  TILE_SCALE * weapon_obj["recoil"], weapon_obj["auto_grab"], weapon_obj["projectile_name"])

# TODO projectile object parsing
