from games.hive.common_functions import axial_distance, find_pieces_around, is_hive_adjacent, is_straight_line, line, move_does_not_break_hive, path_exists
from games.hive.pieces import Ant, Beetle, Grasshopper, Queen, Spider
from games.hive.state import State

def check_move(state, move):
    print(f'Move round {state.round_counter} ',move)
    if move[0][0]:
        return placement_is_allowed(state, move)
    else:
        if move[0][1] != move[1] and is_hive_adjacent(state, move[1]) and move_does_not_break_hive(state, move[0][1], move[1]) and queen_is_on_board(state):
            return piece_valid_move(state, move)
    return False

def piece_valid_move(state, move):
    piece = state.board[move[0][1]][-1]
    if isinstance(piece, Queen):
        if move[1] in state.board.keys(): return False
        return queen_valid_move(state, move)
    elif isinstance(piece, Ant):
        if move[1] in state.board.keys(): return False
        return ant_valid_move(state, move)
    elif isinstance(piece, Grasshopper):
        if move[1] in state.board.keys(): return False
        return grasshopper_valid_move(state, move)
    elif isinstance(piece, Spider):
        if move[1] in state.board.keys(): return False
        return spider_valid_move(state, move)
    elif isinstance(piece, Beetle):
        return beetle_valid_move(state, move)

def queen_valid_move(state, move):
    dist = axial_distance(move[0][1], move[1])
    len_pieces_around = len(find_pieces_around(state, move[0][1]))
    if dist == 1 and len_pieces_around < 5:
        return True
    return False

def ant_valid_move(state, move):
    if path_exists(state, move[0][1], move[1]):
        return True
    return False

def grasshopper_valid_move(state, move):
    # dist > 1, straight line, must hop over pieces
    if axial_distance(move[0][1], move[1]) > 1 and is_straight_line(move[0][1], move[1]):
        return any(p in state.board.keys() for p in line(move[0][1], move[1]))
    return False

def spider_valid_move(state, move):
    if path_exists(state, move[0][1], move[1], spider=True):
        return True
    return False

def beetle_valid_move(state, move):
    if axial_distance(move[0][1], move[1]) == 1:
        return True
    return False
        
def queen_is_on_board(state):
    if state.turn_state != 4:
        return True
    queens = []
    for pieces in state.board.values():
        for piece in pieces: 
            if isinstance(piece, Queen) and piece.color[0]//128 == 2 - state.turn_state:
                return True
    return False


# def game_is_over(state):
#     white_surrounded = False
#     black_surrounded = False
#     for tile in state.get_tiles_with_pieces():
#         for piece in tile.pieces:
#             if type(piece) is pieces.Queen:
#                 adjacent_tiles_with_pieces = [x for x in
#                         tile.adjacent_tiles if x.has_pieces()]
#                 if len(adjacent_tiles_with_pieces) == 6:
#                     if piece.color == PIECE_WHITE:
#                         white_surrounded = True
#                     elif piece.color == PIECE_BLACK:
#                         black_surrounded = True
#                 break
#     if white_surrounded and black_surrounded:
#         return True
#     elif white_surrounded:
#         state.winner = PIECE_BLACK
#         return True
#     elif black_surrounded:
#         state.winner = PIECE_WHITE
#         return True
#     else:
#         return False


def placement_is_allowed(state: State, move):
    if not is_hive_adjacent(state, move[1]):
        return False

    # placed pieces cannot touch other player's pieces to start
    if state.round_counter > 1:
        pieces_around = find_pieces_around(state, move[1])
        for p in pieces_around:
            if p.color[0]//128 != 2 - state.turn_state:
                return False

    if state.turn_state == 1 and state.amount_available_white_pieces[move[0][1][1]] > 0 and not move[1] in state.board.keys():
        return True
    elif state.turn_state == 2 and state.amount_available_black_pieces[move[0][1][1]] > 0 and not move[1] in state.board.keys():
        return True
    return False




# def player_has_no_moves(state):
#     if state.turn % 2 == 1:
#         color = PIECE_WHITE
#     elif state.turn % 2 == 0:
#         color = PIECE_BLACK

#     hive_tiles = state.get_tiles_with_pieces(include_inventory=True)
#     player_piece_tiles = [tile for tile in hive_tiles
#                           if tile.pieces[-1].color == color]
#     open_adjacent_tiles = []

#     for tile in hive_tiles:
#         hive_adjacent_tiles = tile.adjacent_tiles
#         for HA_tile in hive_adjacent_tiles:
#             if HA_tile not in open_adjacent_tiles \
#                 and not HA_tile.has_pieces():
#                 open_adjacent_tiles.append(HA_tile)

#     for old_tile in player_piece_tiles:
#         for new_tile in open_adjacent_tiles:
#             if is_valid_move(state, old_tile, new_tile):
#                 return False

#     return True
