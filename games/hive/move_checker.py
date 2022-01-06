import math
import numpy as np
from copy import deepcopy

from games.hive.const import ANT_ID, BEETLE_ID, GRASSHOPPER_ID, QUEEN_ID, SPIDER_ID
from games.hive.common_functions import axial_distance, find_pieces_around, is_straight_line, neighbours
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
    piece = state.board[move[0][1]]
    if isinstance(piece, Queen):
        return queen_valid_move(state, move)
    elif isinstance(piece, Ant):
        return ant_valid_move(state, move)
    elif isinstance(piece, Grasshopper):
        return grasshopper_valid_move(state, move)
    elif isinstance(piece, Spider):
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
    else:
        return False

def grasshopper_valid_move(state, move):
    # dist > 1, straight line, must hop over pieces
    dist = axial_distance(move[0][1], move[1])

    if dist > 1 and is_straight_line(move[0][1], move[1]):
        return True
        # visited = [old_tile]
        # queue = [old_tile]
        # while queue and new_tile not in visited:
        #     current_tile = queue.pop(0)
        #     for neighbor_tile in [x for x in
        #             current_tile.adjacent_tiles if x.has_pieces()
        #             and is_straight_line(old_tile.axial_coords,
        #             x.axial_coords)]:
        #         if neighbor_tile not in visited:
        #             visited.append(neighbor_tile)
        #             queue.append(neighbor_tile)

        # # have to check last tile seperately bc it will never have a piece

        # for penultimate_tile in [x for x in new_tile.adjacent_tiles
        #         if x.has_pieces()]:
        #     if penultimate_tile in visited \
        #         and is_straight_line(old_tile.axial_coords,
        #             new_tile.axial_coords):
        #         return True
    else:
        return False

def spider_valid_move(state, move):
    if path_exists(state, move[0][1], move[1], spider=True):
        return True
    else:
        return False

def beetle_valid_move(state, move):
    dist = axial_distance(move[0][1], move[1])
    if dist == 1:
    # if dist == 1 and (move_is_not_blocked_or_jump(state, old_tile,
    #                     new_tile) or new_tile.has_pieces()
    #                     or len(old_tile.pieces) > 1):

        # can't slide into a blocked hex but it can go up or down into one

        return True
    else:
        return False

# def is_valid_move(state, old_tile, new_tile):
#     base_move_check = new_tile is not None and new_tile.coords \
#         != old_tile.coords and (not new_tile.has_pieces()
#                                 or type(state.moving_piece)
#                                 is pieces.Beetle)
#     full_move_check = base_move_check \
#         and new_tile.is_hive_adjacent(state) \
#         and move_does_not_break_hive(state, old_tile) \
#         and (placement_is_allowed(state, old_tile, new_tile)
#              or state.moving_piece.move_is_valid(state, old_tile,
#              new_tile))
#     if state.turn == 1:
#         if base_move_check and type(new_tile) is tile.Start_Tile:
#             return True
#     elif state.turn == 2:
#         if base_move_check and new_tile.is_hive_adjacent(state):
#             return True
#     elif state.turn <= 6 and state.turn >= 3:
#         if full_move_check and queen_is_on_board(state, old_tile):
#             return True
#     elif state.turn == 7 or state.turn == 8:
#         if full_move_check and move_obeys_queen_by_4(state):
#             return True
#     else:
#         if full_move_check:
#             return True
#     return False

def is_hive_adjacent(state, coordinate):
    if len(state.board) == 0:
        return True
    for piece in state.board.keys():
        if axial_distance(piece, coordinate) == 1:
            return True        
    return False

def queen_is_on_board(state):
    if state.turn_state != 4:
        return True
    queens = [q for q in state.board.values() if isinstance(q, Queen) and q.color[0]//128 == 2 - state.turn_state]
    if len(queens) == 1:
        return True
    return False

def move_does_not_break_hive(state, coordinates, additional_coordiantes = None):
    copy_state = deepcopy(state)
    del copy_state.board[coordinates]

    if additional_coordiantes is not None:
        copy_state.board[additional_coordiantes] = None

    tile_list = list(copy_state.board.keys())
    visited = []
    queue = []

    visited.append(tile_list[0])
    queue.append(tile_list[0])

    while queue:
        current = queue.pop(0)

        for neighbor in [x for x in neighbours(current)
                              if x in copy_state.board.keys()]:
            if neighbor not in visited:
                visited.append(neighbor)
                queue.append(neighbor)

    if len(visited) != len(tile_list):
        return False
    else:
        return True


# def queen_is_on_board(state, old_tile):
#     if old_tile.axial_coords == (99, 99):  # placements are ok
#         return True
#     else:

#          # allow move if queen is down for that color

#         if state.turn % 2 == 1:
#             color = PIECE_WHITE
#         else:
#             color = PIECE_BLACK
#         for tile in state.get_tiles_with_pieces():
#             for piece in tile.pieces:
#                 if type(piece) is pieces.Queen and piece.color == color:
#                     return True
#     return False


# def move_obeys_queen_by_4(state):
#     queens_on_board = []
#     for tile in state.get_tiles_with_pieces():
#         for piece in tile.pieces:
#             if type(piece) is pieces.Queen:
#                 queens_on_board.append(piece)

#     if len(queens_on_board) == 2:
#         return True
#     elif len(queens_on_board) == 0:
#         if state.turn == 7 and type(state.moving_piece) is pieces.Queen \
#             and state.moving_piece.color == PIECE_WHITE:
#             return True
#         elif state.turn == 8 and type(state.moving_piece) \
#             is pieces.Queen and state.moving_piece.color == PIECE_BLACK:
#             return True
#     elif len(queens_on_board) > 0:
#         if queens_on_board[0].color == PIECE_WHITE and state.turn == 7:
#             return True
#         elif queens_on_board[0].color == PIECE_BLACK and state.turn \
#             == 7 and type(state.moving_piece) is pieces.Queen:
#             return True
#         elif queens_on_board[0].color == PIECE_BLACK and state.turn \
#             == 8:
#             return True
#         elif queens_on_board[0].color == PIECE_WHITE and state.turn \
#             == 8 and type(state.moving_piece) is pieces.Queen:
#             return True

#     return False


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

def path_exists(state, coord1, coord2, spider=False):
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
