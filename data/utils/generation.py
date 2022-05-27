from typing import Tuple, List

from numpy import ndarray, zeros, array, random, argwhere, invert, amin, sign, ndenumerate, empty
from numpy.random import randint
from pygame import Rect, Surface
from scipy.ndimage.measurements import label
from scipy.spatial.distance import cdist

from data.objects.bonus_data import Bonus
from data.objects.player_data import Player
from data.objects.tile_data import Tile
from data.utils.constants import TILE_SIZE, GRID_SIZE, NOISE_DENSITY, AUTOMATON_ITERATION, GRID_HEIGHT, \
    PLAYER_SIZE, BONUS_REPARTITION, BONUS_SIZE, PLAYER_SPAWN_HEIGHT, TILE_SPRITES


def _get_neighbors_count_grid(grid: ndarray) -> ndarray:
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


def _cartesian_list():
    """
    Returns a list of all possible combinations of 4 neighbors.

    :return: all possible combinations of 4 neighbors
    """
    cartesian_product: List = []
    for a in [False, True]:
        for b in [False, True]:
            for c in [False, True]:
                for d in [False, True]:
                    cartesian_product.append([a, b, c, d])
    return cartesian_product


def _get_von_neumann_neighborhood(grid: ndarray, idx: ndarray) -> ndarray:
    """
    Returns respectively up, right, down and left neighbors of the given index.

    :param grid: boolean grid
    :param idx: index
    :return: von neumann neighborhood of index
    """
    offsets: ndarray = array(((0, -1), (1, 0), (0, 1), (-1, 0)))

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


def _to_tiles(grid: ndarray) -> ndarray:
    """
    Returns a grid with the corresponding tile data for each cell.

    :param grid: boolean grid
    :return: tile grid
    """
    tile_grid: ndarray = empty(grid.shape).astype(Tile)
    neighbor_patterns: List = _cartesian_list()

    for (i, j), cell in ndenumerate(grid):
        if cell:
            idx: ndarray = array((i, j))
            neighbors: ndarray = _get_von_neumann_neighborhood(grid, idx)
            # print(idx, neighbors, neighbor_patterns.index(list(neighbors)))

            # choosing tile sprite depending on neighborhood
            sprite: Surface = TILE_SPRITES[neighbor_patterns.index(list(neighbors))]
            tile_grid[i, j] = Tile(Rect(idx * TILE_SIZE, tuple(TILE_SIZE)), sprite)
        else:
            tile_grid[i, j] = None

    return tile_grid


def generate_world() -> Tuple[ndarray, Player, ndarray]:
    """
    Returns a world grid containing the wall tiles, and none for the empty tiles.
    Returns also the player, and the list of spawned bonuses.

    Algorithm uses procedural cave generation with cellular automaton and generation of connections between rooms.
    https://www.youtube.com/playlist?list=PLFt_AvWsXl0eZgMK_DT5_biRkWXftAOf9

    Implementation uses uniform vectorization.
    https://lhoupert.fr/test-jbook/04-code-vectorization.html

    :return: tile grid, player, bonuses
    """

    # Cellular automaton ------------------------------------------------------

    # initial noise grid
    bool_grid: ndarray = random.choice(
        a=[True, False],
        size=GRID_SIZE,
        p=[NOISE_DENSITY, 1 - NOISE_DENSITY]
    )

    # number of wall tiles neighbors for each cell
    n_count_grid: ndarray = _get_neighbors_count_grid(bool_grid)

    # cellular automaton execution
    for _ in range(AUTOMATON_ITERATION):
        # resetting neighbors count
        n_count_grid = _get_neighbors_count_grid(bool_grid)

        # flatten grids
        bool_grid_flat: ndarray = bool_grid.ravel()
        n_count_grid_flat: ndarray = n_count_grid.ravel()

        # rules application
        bool_grid_flat[argwhere(n_count_grid_flat > 4)] = True
        bool_grid_flat[argwhere(n_count_grid_flat <= 3)] = False

        # border tiles are walls
        bool_grid[0, :] = bool_grid[-1, :] = bool_grid[:, 0] = bool_grid[:, -1] = True

    # Rooms connections -------------------------------------------------------

    # localizing rooms of empty tiles
    room_grid, n_rooms = label(invert(bool_grid))

    # matrix indicating if two rooms are connected between each other
    connections: ndarray = zeros((n_rooms, n_rooms), dtype=bool)

    connections_idxes: List = []  # TODO find size of this thing in advance

    # starting from room 1 because room 0 contains all the wall tiles
    for a in range(1, n_rooms):
        for b in range(1, n_rooms):

            # skipping to next room if the two rooms are the same
            # or if they are already connected
            if a == b or connections[a, b] or connections[b, a]:
                continue

            # indexes of rooms contours
            contours_a_idxes: ndarray = argwhere((room_grid == a) & (n_count_grid > 0))
            contours_b_idxes: ndarray = argwhere((room_grid == b) & (n_count_grid > 0))

            # matrix of distances between each contours
            distances: ndarray = cdist(contours_a_idxes, contours_b_idxes)

            # finding the smallest distance index
            min_dist_idx: ndarray = argwhere(distances == amin(distances))[0]

            # getting the two closest tiles, ie the two connection line ends
            tile_a_idx: ndarray = contours_a_idxes[min_dist_idx[0]]
            tile_b_idx: ndarray = contours_b_idxes[min_dist_idx[1]]

            # marking the two rooms as connected
            connections[a, b] = connections[b, a] = True

            # adding the two points to our list of connections
            connections_idxes.append((tile_a_idx, tile_b_idx))

    connections_idxes: ndarray = array(connections_idxes, dtype=int)

    # Digging connections -----------------------------------------------------

    for connection in connections_idxes:

        x: int = connection[0, 0]
        y: int = connection[0, 1]

        dx: int = connection[1, 0] - x
        dy: int = connection[1, 1] - y

        inverted: bool = False
        step: int = sign(dx)
        step_grad: int = sign(dy)
        longest: int = abs(dx)
        shortest: int = abs(dy)

        if longest < shortest:
            inverted = True
            step = sign(dy)
            step_grad = sign(dx)
            longest = abs(dy)
            shortest = abs(dx)

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
        if False not in bool_grid[line[1:-1, 0], line[1:-1, 1]]:
            # digging in a cross pattern to ensure space for player
            bool_grid[line[:, 0], line[:, 1]] = \
                bool_grid[line[:, 0] + 1, line[:, 1]] = \
                bool_grid[line[:, 0] - 1, line[:, 1]] = \
                bool_grid[line[:, 0], line[:, 1] + 1] = \
                bool_grid[line[:, 0], line[:, 1] - 1] = False

    # ensuring borders are walls, one last time
    bool_grid[0, :] = bool_grid[-1, :] = bool_grid[:, 0] = bool_grid[:, -1] = True

    # Player ------------------------------------------------------------------

    # choosing free tile to spawn on
    empty_xs: ndarray = argwhere(bool_grid[:, PLAYER_SPAWN_HEIGHT] == False)
    x: int = int(empty_xs[randint(0, empty_xs.size - 1)])  # FIXME sometimes crashes (full row ?)

    player_idx: ndarray = array((x, PLAYER_SPAWN_HEIGHT))  # grid space
    player_pos = player_idx * TILE_SIZE + TILE_SIZE / 2 - PLAYER_SIZE / 2  # world space
    player = Player(player_pos.astype(float), Rect(tuple(player_pos), tuple(PLAYER_SIZE)))

    # TODO top exit generation ------------------------------------------------

    # Bonuses -----------------------------------------------------------------

    bonuses: List = []
    for y in range(GRID_HEIGHT - BONUS_REPARTITION, 0, -BONUS_REPARTITION):

        empty_xs: ndarray = argwhere(bool_grid[:, y] == False)
        if empty_xs.size > 1:
            x: int = int(empty_xs[randint(0, empty_xs.size - 1)])

            bonus_pos: ndarray = array((x, y), dtype=float) * TILE_SIZE + TILE_SIZE / 2 - BONUS_SIZE / 2
            bonus_rect: Rect = Rect(tuple(bonus_pos), tuple(BONUS_SIZE))
            bonuses.append(Bonus(bonus_rect, array(bonus_rect.topleft, dtype=float)))

    # Convert to grid of tiles ------------------------------------------------

    tile_grid: ndarray = _to_tiles(bool_grid)

    return tile_grid, player, array(bonuses)
