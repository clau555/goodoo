from dataclasses import replace

from numpy import array, ndarray

from src.model.dataclasses import Mushroom, Player, TileMaps
from src.model.utils import world_to_grid


def damage_mushroom(tile_maps: TileMaps, player: Player) -> TileMaps:
    """
    Lower collided mushrooms health by one.
    Replace them by None if their health reaches 0.

    :param tile_maps: tile maps data
    :param player: player data
    :return: updated tile maps data
    """
    cave_: ndarray = tile_maps.cave

    for mushroom in player.colliding_mushrooms:
        mushroom_: Mushroom = replace(mushroom, health=mushroom.health - 1)
        grid_pos: ndarray = world_to_grid(array(mushroom.rect.center))

        if mushroom_.health < 1:
            cave_[grid_pos[0], grid_pos[1]] = None
        else:
            cave_[grid_pos[0], grid_pos[1]] = mushroom_

    return replace(tile_maps, cave=cave_)


def add_mushrooms(shaking_mushrooms: list[Mushroom], player: Player) -> list[Mushroom]:
    """
    Adds mushrooms to the list of shaking mushrooms.

    :param shaking_mushrooms: list of shaking mushrooms
    :param player: player data
    :return: updated list of shaking mushrooms
    """
    shaking_mushrooms_: list[Mushroom] = shaking_mushrooms
    for mushroom in player.colliding_mushrooms:
        if mushroom not in shaking_mushrooms:
            shaking_mushrooms_.append(mushroom)
    return shaking_mushrooms_


def update_shaking_mushrooms(shaking_mushrooms: list[Mushroom], delta_time: float) -> list[Mushroom]:
    """
    Updates the shaking mushroom counter of every mushroom in the list.
    Removes the mushroom from the list if its counter reaches 0.

    :param shaking_mushrooms: list of shaking mushrooms
    :param delta_time: time since last frame
    :return: updated list of shaking mushrooms
    """
    shaking_mushrooms_: list[Mushroom] = []

    # adding mushrooms colliding with player to the list
    for mushroom in shaking_mushrooms:
        mushroom = replace(mushroom, shake_counter=mushroom.shake_counter - delta_time)
        shaking_mushrooms_.append(mushroom)

    # removing mushrooms who ended their animation
    shaking_mushrooms_ = list(filter(_is_mushroom_shaking, shaking_mushrooms_))

    return shaking_mushrooms_


def _is_mushroom_shaking(mushroom: Mushroom) -> bool:
    """
    :param mushroom: mushroom data
    :return: true if mushroom is still shaking
    """
    return mushroom.shake_counter > 0
