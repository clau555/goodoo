from math import radians
from typing import Tuple, List

from numpy import ndarray, zeros, array, argwhere, invert, amin, sign, ndenumerate, empty, int8, cos, sin
from numpy.random import randint, random_sample, choice
from pygame import Rect, Surface
from pygame.transform import rotate
from scipy.ndimage.measurements import label
from scipy.spatial.distance import cdist

from src.model.constants import TILE_SIZE, GRID_SIZE, NOISE_DENSITY, AUTOMATON_ITERATION, GRID_HEIGHT, \
    PLAYER_SIZE, TILE_SPRITES, GRID_WIDTH, OBSTACLE_MAX_DENSITY, AMETHYST_DENSITY, \
    ObstacleType, OBSTACLE_SPRITES
from src.model.dataclasses import Player, Tile, Obstacle
from src.model.utils import moore_neighborhood


def generate_world() -> Tuple[ndarray, Player]:
    """
    Returns a world grid containing the wall tiles, and none for the empty tiles.
    Returns also the player.

    :return: tile grid and player data
    """
    cave: ndarray = _generate_cave()
    cave = _generate_exit(cave)
    cave = _generate_connections(cave, _rooms_connections_points(cave))

    return _generate_tiles(cave), _spawn_player(cave)


def _generate_cave() -> ndarray:
    """
    Generates a cave of booleans (true = wall, false = empty) using cellular automaton.

    https://youtu.be/v7yyZZjF1z4
    https://lhoupert.fr/test-jbook/04-code-vectorization.html

    :return: boolean grid
    """

    # initial noise grid
    cave: ndarray = choice(
        a=(True, False),
        size=GRID_SIZE,
        p=[NOISE_DENSITY, 1 - NOISE_DENSITY]
    )

    # cellular automaton execution
    for _ in range(AUTOMATON_ITERATION):
        # number of wall tiles neighbors for each cell
        n_count_grid = _neighbors_count_grid(cave)

        # flatten grids
        cave_flat: ndarray = cave.ravel()
        n_count_grid_flat: ndarray = n_count_grid.ravel()

        # rules application
        cave_flat[argwhere(n_count_grid_flat > 4)] = True
        cave_flat[argwhere(n_count_grid_flat <= 3)] = False

        # border tiles are walls during generation
        cave[0, :] = cave[-1, :] = cave[:, 0] = cave[:, -1] = True

    return cave


def _generate_exit(cave: ndarray) -> ndarray:
    """
    Generates an exit in the cave by digging a circle at the top of the cave.

    :param cave: boolean grid
    :return: updated boolean grid
    """
    cave_ = array(cave)
    exit_coords: ndarray = abs(_circle_coords(array((GRID_WIDTH // 2, 0)), GRID_WIDTH // 2 - 1))
    cave_[exit_coords[:, 0], exit_coords[:, 1]] = False
    cave_[:, 0] = False
    return cave_


def _rooms_connections_points(cave: ndarray) -> ndarray:
    """
    Generates the points where the rooms will be connected.

    https://youtu.be/eVb9kQXvEZM

    :param cave: boolean grid
    :return: array of points
    """

    # number of wall tiles neighbors for each cell
    n_count_grid: ndarray = _neighbors_count_grid(cave)

    # localizing rooms of empty tiles
    room_grid, n_rooms = label(invert(cave))

    # matrix indicating if two rooms are connected between each other
    connections: ndarray = zeros((n_rooms, n_rooms), dtype=bool)

    connections_idxes: List = []

    # starting from room 1 because room 0 contains all the wall tiles
    for room_a_idx in range(1, n_rooms):
        for room_b_idx in range(1, n_rooms):

            # skipping to next room if the two rooms are the same
            # or if they are already connected
            if room_a_idx == room_b_idx or connections[room_a_idx, room_b_idx] or connections[room_b_idx, room_a_idx]:
                continue

            # indexes of rooms contours
            contours_a_idxes: ndarray = argwhere((room_grid == room_a_idx) & (n_count_grid > 0))
            contours_b_idxes: ndarray = argwhere((room_grid == room_b_idx) & (n_count_grid > 0))

            # matrix of distances between each contours
            distances: ndarray = cdist(contours_a_idxes, contours_b_idxes)

            # finding the smallest distance index
            min_dist_idx: ndarray = argwhere(distances == amin(distances))[0]

            # getting the two closest tiles, ie the two connection line ends
            tile_a_idx: ndarray = contours_a_idxes[min_dist_idx[0]]
            tile_b_idx: ndarray = contours_b_idxes[min_dist_idx[1]]

            # marking the two rooms as connected
            connections[room_a_idx, room_b_idx] = connections[room_b_idx, room_a_idx] = True

            # adding the two points to our list of connections
            connections_idxes.append((tile_a_idx, tile_b_idx))

    return array(connections_idxes, dtype=int)


def _generate_connections(cave: ndarray, connections_points: ndarray) -> ndarray:
    """
    Generates the connections between the rooms.

    https://youtu.be/7RiGikVLS3c

    :param cave: boolean grid
    :param connections_points: array of points
    :return: updated boolean grid
    """

    for connection in connections_points:

        x: int = connection[0, 0]
        y: int = connection[0, 1]

        d_x: int = connection[1, 0] - x
        d_y: int = connection[1, 1] - y

        inverted: bool = False
        step: int = sign(d_x)
        step_grad: int = sign(d_y)
        longest: int = abs(d_x)
        shortest: int = abs(d_y)

        if longest < shortest:
            inverted = True
            step = sign(d_y)
            step_grad = sign(d_x)
            longest = abs(d_y)
            shortest = abs(d_x)

        grad: float = longest / 2

        # will store tile coordinates which are on the current line
        line: ndarray = zeros((longest, 2), dtype=int)

        for i in range(longest):
            line[i] = array((x, y))

            if inverted:
                y += step
            else:
                x += step

            grad += shortest

            if grad >= longest:
                if inverted:
                    x += step_grad
                else:
                    y += step_grad
                grad -= longest

        # making sure the path doesn't cross another room
        if False not in cave[line[1:-1, 0], line[1:-1, 1]]:
            # digging in a cross pattern to ensure space for player
            cave[line[:, 0], line[:, 1]] = \
                cave[line[:, 0] + 1, line[:, 1]] = \
                cave[line[:, 0] - 1, line[:, 1]] = \
                cave[line[:, 0], line[:, 1] + 1] = \
                cave[line[:, 0], line[:, 1] - 1] = False

    # ensuring borders are walls, except for the top which is the exit
    cave[0, :] = cave[-1, :] = cave[:, -1] = True

    return cave


def _spawn_player(cave: ndarray) -> Player:
    """
    Spawns the player in the cave by searching for the most bottom free tile.
    :param cave: boolean grid
    :return: player
    """

    # getting the first row with empty tiles starting from bottom of the grid
    spawn_height: int = GRID_HEIGHT - 1
    empty_xs: ndarray = argwhere(cave[:, spawn_height])
    for j in range(GRID_HEIGHT - 1, 0, -1):
        empty_xs = argwhere(cave[:, j] == False)  # have to do this boolean comparison because of numpy
        if empty_xs.size > 0:
            spawn_height = j
            break

    if empty_xs.size == 0:
        raise ValueError("No player spawn point found")
    if empty_xs.size == 1:
        x: int = int(empty_xs[0])  # choosing the only empty tile
    else:
        x: int = int(empty_xs[randint(0, empty_xs.size - 1)])  # choosing a random empty tile

    player_idx: ndarray = array((x, spawn_height))  # grid space
    player_pos = player_idx * TILE_SIZE + TILE_SIZE / 2 - PLAYER_SIZE / 2  # world space
    return Player(player_pos.astype(float), Rect(tuple(player_pos), tuple(PLAYER_SIZE)))


def _neighbors_count_grid(grid: ndarray) -> ndarray:
    """
    Returns a grid with the number of neighbors for each cell.
    A neighbor is counted if it's true.

    :param grid: boolean grid
    :return: grid with the number of neighbors for each cell
    """
    neighbors_mat: ndarray = zeros(grid.shape, dtype=int)
    int_grid: ndarray = grid.astype(int)
    neighbors_mat[1:-1, 1:-1] = (int_grid[:-2, :-2] + int_grid[:-2, 1:-1] + int_grid[:-2, 2:]
                                 + int_grid[1:-1, :-2] + int_grid[1:-1, 2:] + int_grid[2:, :-2]
                                 + int_grid[2:, 1:-1] + int_grid[2:, 2:])
    return neighbors_mat


def _circle_coords(center: ndarray, radius: int) -> ndarray:
    """
    Returns the list of coordinates inside the circle.

    https://stackoverflow.com/a/39862846/17987233

    :param center: circle center
    :param radius: circle radius
    :return: list of coordinates inside the circle
    """
    coords: List = []

    x = radius
    for x_ in range(-x, x + 1):
        y = int((radius ** 2 - x_ ** 2) ** 0.5)
        for y_ in range(-y, y + 1):
            coords.append(array((x_, y_)))

    return array(coords) + center


def _generate_tiles(grid: ndarray) -> ndarray:
    """
    Returns a grid with the corresponding tile data for each cell.

    :param grid: boolean grid
    :return: tile grid
    """

    # output grid
    tile_cave: ndarray = empty(grid.shape).astype(Tile)

    # all neumann neighborhood combinations possible
    neighbor_patterns: List = _cartesian_list()

    # input grid but with integers (used for obstacles generation)
    # 0 = no tile, 1 = tile, 2 = obstacle
    grid_with_obstacles: ndarray = array(grid, copy=True, dtype=int8)

    for (i, j), cell in ndenumerate(grid):

        idx: ndarray = array((i, j))
        neumann_neighbors: ndarray = _neumann_neighborhood(grid, idx)
        angle: int = _obstacle_angle(moore_neighborhood(grid_with_obstacles, idx))

        # converting bool to tile
        if cell:
            # choosing tile sprite depending on neighborhood
            sprite: Surface = TILE_SPRITES[neighbor_patterns.index(list(neumann_neighbors))]
            tile_cave[i, j] = Tile(Rect(idx * TILE_SIZE, tuple(TILE_SIZE)), sprite)

        # adding randomly obstacle on empty tile
        # the higher the tile the more it's likely to spawn
        elif random_sample() < OBSTACLE_MAX_DENSITY * (GRID_HEIGHT - j) / GRID_HEIGHT and angle:
            type_: ObstacleType = ObstacleType.AMETHYST if random_sample() > AMETHYST_DENSITY else ObstacleType.MUSHROOM
            sprite: Surface = OBSTACLE_SPRITES[type_]
            tile_cave[i, j] = _spawn_obstacle(idx, angle, sprite, type_)
            grid_with_obstacles[i, j] = 2  # marking this tile as occupied by an obstacle

        else:
            tile_cave[i, j] = None

    return tile_cave


def _neumann_neighborhood(grid: ndarray, idx: ndarray) -> ndarray:
    """
    Returns respectively up, right, down and left neighbors of the given index.

    :param grid: boolean grid
    :param idx: index
    :return: von neumann neighborhood of index
    """
    offsets: ndarray = array(((0, -1), (1, 0), (0, 1), (-1, 0)))

    # TODO are you sure about that?
    if idx[0] == 0:
        offsets[3] = zeros(2)
    elif idx[0] == grid.shape[0] - 1:
        offsets[1] = zeros(2)
    if idx[1] == 0:
        offsets[0] = zeros(2)
    elif idx[1] == grid.shape[1] - 1:
        offsets[2] = zeros(2)

    offset_idxes: ndarray = idx + offsets

    return grid[offset_idxes[:, 0], offset_idxes[:, 1]]


def _cartesian_list() -> List:
    """
    Returns a list of all possible combinations of 4 neighbors.

    :return: all possible combinations of 4 neighbors
    """
    cartesian_product: List = []
    for bit_1 in [False, True]:
        for bit_2 in [False, True]:
            for bit_3 in [False, True]:
                for bit_4 in [False, True]:
                    cartesian_product.append([bit_1, bit_2, bit_3, bit_4])
    return cartesian_product


def _obstacle_angle(moore_neighbors: ndarray) -> int:
    """
    Returns the angle of an obstacle given its moore neighborhood (90, 180 or 270 degrees).
    Returns zero if the obstacle is not placeable.

    :param moore_neighbors: moore neighborhood of the obstacle, contains integers (0 = no tile, 1 = tile, 2 = obstacle).
    :return: degree angle of the obstacle
    """
    if 2 in moore_neighbors:
        return 0
    if moore_neighbors[-1, :].all() and not moore_neighbors[:-1, :].any():
        return 90
    if moore_neighbors[:, 0].all() and not moore_neighbors[:, 1:].any():
        return 180
    if moore_neighbors[0, :].all() and not moore_neighbors[1:, :].any():
        return 270
    return 0


def _spawn_obstacle(idx: ndarray, angle: int, sprite: Surface, type_: ObstacleType) -> Obstacle:
    """
    Returns an obstacle from the given parameters.

    :type idx: index of the tile
    :type angle: degree angle at which the amethyst will be spawned
    :param sprite: sprite of the obstacle
    :param type_: type of the obstacle (AMETHYST or MUSHROOM)
    :return: obstacle data
    """
    return Obstacle(
        Rect(idx * TILE_SIZE, tuple(TILE_SIZE)),
        rotate(sprite, angle),
        array((round(cos(radians(90 + angle))), -round(sin(radians(90 + angle))))),
        type_
    )
