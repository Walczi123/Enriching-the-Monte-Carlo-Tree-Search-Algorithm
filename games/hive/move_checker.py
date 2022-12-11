from games.hive.common_functions import axial_distance, find_pieces_around, is_hive_adjacent, is_straight_line, line, move_does_not_break_hive, path_exists
from games.hive.const import QUEEN_ID
from games.hive.pieces import Ant, Beetle, Grasshopper, Queen, Spider
from games.hive.state import State

def check_move(state, move):
    if move[0][0]:
        return placement_is_allowed(state, move) and queen_is_on_board(state, move)
    else:
        if move[0][1] != move[1] and move_does_not_break_hive(state, move[0][1]) and queen_is_on_board(state):
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
        
def queen_is_on_board(state:State, move=None):
    if state.round_counter != 4:
        return True

    if move and move[0][1][1] == QUEEN_ID:
        return True

    for pieces in state.board.values():
        for piece in pieces: 
            if isinstance(piece, Queen) and piece.color[0]//128 == 2 - state.turn_state:
                return True
    return False

def placement_is_allowed(state: State, move):
    if move[1] in state.board.keys():
        return False
    if not is_hive_adjacent(state, move[1]):
        return False
    if state.round_counter > 1:
        pieces_around = find_pieces_around(state, move[1])
        for p in pieces_around:
            if p.color[0]//128 != 2 - state.turn_state:
                return False
    if state.turn_state == 1 and state.amount_available_white_pieces[move[0][1][1]] > 0:
        return True
    elif state.turn_state == 2 and state.amount_available_black_pieces[move[0][1][1]] > 0:
        return True
    return False
