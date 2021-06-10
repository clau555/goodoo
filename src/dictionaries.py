import json
from typing import IO


def get_objects_dict(name: str) -> dict:
    """
    Returns the dictionary created from the json file
    corresponding to the name passed in argument.\n
    :param name: json file name
    :return: dictionary corresponding to the json file
    """
    file: IO = open("data/" + name + ".json")
    data: dict = json.load(file)
    file.close()
    return data


WEAPONS_DICT: dict = get_objects_dict("weapons")
BONUSES_DICT: dict = get_objects_dict("bonuses")
PROJECTILES_DICT: dict = get_objects_dict("projectiles")
