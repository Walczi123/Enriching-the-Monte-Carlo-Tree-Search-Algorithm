#https://www[0]edblobgames.com/grids/hexagons/#distances
def cube_to_axial(cube):
    q = cube[0]
    r = cube[1]
    return (q, r)

def axial_to_cube(hex):
    q = hex[0]
    r = hex[1]
    s = -q-r
    return (q, r, s)

def axial_to_oddr(hex):
    col = hex[0] + (hex[1] - (hex[1]&1)) / 2
    row = hex[1]
    return (col, row)

def oddr_to_axial(hex):
    q = hex[0] + (hex[1] - (hex[1]&1)) / 2
    r = hex[1]
    return (q, r)

def cube_distance(a, b):
    return (abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])) / 2

def axial_distance(a, b):
    return cube_distance(evenr_to_axial(a),evenr_to_axial(b))

def evenr_to_axial(hex):
    q = hex[0] - (hex[1] + (hex[1]&1)) / 2
    r = hex[1]
    return (q, r, -q-r)

def is_straight_line(coords1, coords2):
    (x1, y1, z1) = evenr_to_axial(coords1)
    (x2, y2, z2) = evenr_to_axial(coords2)

    return x1 == x2 or y1 == y2 or z1 == z2

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
    return [state.board[n] for n in neighbours(coordinates) if n in state.board.keys()]