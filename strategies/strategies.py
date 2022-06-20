from copy import deepcopy
import random
from shutil import move
        

def random_strategy(moves, state, board_move, get_all_posible_moves, player, change_player):
    return random.choice(moves)

def mobility_strategy(moves, state, board_move, get_all_posible_moves, player, change_player):
    n_moves = []
    for i in range(len(moves)):
        iteration_state = deepcopy(state)
        state_after_move = board_move(iteration_state, moves[i], player)
        n_moves.append(len(get_all_posible_moves(state_after_move, change_player(player))))
    index = n_moves.index(min(n_moves))
    return moves[index]

def mobility_strategy_vs(moves, state, board_move, get_all_posible_moves, player, change_player):
    n_moves = []
    for i in range(len(moves)):
        iteration_state = deepcopy(state)
        state_after_move = board_move(iteration_state, moves[i], player)
        n_moves_p1 = len(get_all_posible_moves(state_after_move, player))
        n_moves_p2 = len(get_all_posible_moves(state_after_move, change_player(player)))
        n_moves.append(n_moves_p1 - n_moves_p2)
    index = n_moves.index(max(n_moves))
    return moves[index]