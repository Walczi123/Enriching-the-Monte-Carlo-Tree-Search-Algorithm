#https://www[0]edblobgames.com/grids/hexagons/#distances
from copy import deepcopy

from games.hive.state import State


def cube_to_axial(cube):
    q = cube[0]
    r = cube[1]
    return (q, r)

def axial_to_cube(hex):
    q = hex[0]
    r = hex[1]
    s = -q-r
    return (q, r, s)

def cube_distance(a, b):
    return (abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])) / 2

def axial_distance(a, b):
    return cube_distance(evenr_to_axial(a),evenr_to_axial(b))

def evenr_to_axial(hex):
    q = hex[0] - (hex[1] + (hex[1]&1)) / 2
    r = hex[1]
    return (q, r, -q-r)

def axial_to_evenr(hex):
    col = hex[0] + (hex[1] + (hex[1]&1)) / 2
    row = hex[1]
    return (col, row) 

def is_straight_line(coords1, coords2):
    (x1, y1, z1) = evenr_to_axial(coords1)
    (x2, y2, z2) = evenr_to_axial(coords2)

    return x1 == x2 or y1 == y2 or z1 == z2

def lerp(a, b, t): # for floats
    return a + (b - a) * t

def cube_lerp(a, b, t): # for hexes
    return (lerp(a[0], b[0], t),
            lerp(a[1], b[1], t),
            lerp(a[2], b[2], t))

def cube_line(a, b):
    N = int(cube_distance(a, b))
    results = []
    for i in range(N):
        results.append(cube_round(cube_lerp(a, b, 1.0/N * i)))
    return results

def line(a,b):
    return [axial_to_evenr(c) for c in cube_line(evenr_to_axial(a), evenr_to_axial(b))]

def cube_round(frac):
    q = round(frac[0])
    r = round(frac[1])
    s = round(frac[2])

    q_diff = abs(q - frac[0])
    r_diff = abs(r - frac[1])
    s_diff = abs(s - frac[2])

    if q_diff > r_diff and q_diff > s_diff:
        q = -r-s
    elif r_diff > s_diff:
        r = -q-s
    else:
        s = -q-r

    return (q, r, s)

def neighbours(coordinate):
    """Returns cube hex neighbours"""
    neighbours = [
        (coordinate[0] + 1, coordinate[1]    ),
        (coordinate[0]    , coordinate[1] + 1),
        (coordinate[0] - 1, coordinate[1]    ),
        (coordinate[0]    , coordinate[1] - 1),
        ]
    if coordinate[1] % 2:
        neighbours.append((coordinate[0] - 1, coordinate[1] - 1))
        neighbours.append((coordinate[0] - 1, coordinate[1] + 1))
    else:
        neighbours.append((coordinate[0] + 1, coordinate[1] - 1))
        neighbours.append((coordinate[0] + 1, coordinate[1] + 1))
    return neighbours

def find_pieces_around(state, coordinates):
    res = []
    for n in neighbours(coordinates):
        if n in state.board.keys():
            res.extend(state.board[n])
    return res

def path_exists(state:State, coord1, coord2, spider=False):
    queue = []
    queue.append([coord1])

    while queue:
        path = queue.pop(0)
        current_tile = path[-1]
        if spider:
            if current_tile == coord2 and len(path) - 1 == 3:
                return True
        elif current_tile == coord2:
            return True

        for neighbor_tile in [x for x in neighbours(current_tile)
                              if is_hive_adjacent(state, x)
                              and not x in state.board.keys()]:
            if neighbor_tile not in path:
                new_path = list(path)
                new_path.append(neighbor_tile)
                queue.append(new_path)

    return False

def is_hive_adjacent(state:State, coordinate):
    if len(state.board) == 0:
        return True
    for piece in state.board.keys():
        if axial_distance(piece, coordinate) == 1:
            return True        
    return False

def is_hive_adjacent_coordinates(coordinates, coordinate):
    if len(coordinates) == 0:
        return True
    for piece in coordinates:
        if axial_distance(piece, coordinate) == 1:
            return True        
    return False

def move_does_not_break_hive(state:State, coordinates):
    copy_state = deepcopy(state)
    copy_state.remove_from_board(coordinates, copy_state.board[coordinates][-1])
    return one_hive(copy_state.board.keys())

def one_hive(coordinates):
    unvisited = set(coordinates)
    todo = [unvisited.pop()]
    while todo:
        node = todo.pop()
        for neighbour in neighbours(node):
            if neighbour in unvisited:
                unvisited.remove(neighbour)
                todo.append(neighbour)
    return not unvisited