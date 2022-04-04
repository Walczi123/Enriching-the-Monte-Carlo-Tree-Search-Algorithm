import random
from shutil import move
        

def random_strategy(moves, board_move, get_all_posible_moves, player, change_player):
    return random.choice(moves)

def mobility_strategy(moves, board_move, get_all_posible_moves, player, change_player):
    n_moves = []
    for i in len(moves):
        state_after_move = board_move(moves[i])
        n_moves.append(get_all_posible_moves(state_after_move, player))
    index = n_moves.index(max(n_moves))
    return n_moves[index]

def mobility_strategy_vs(moves, board_move, get_all_posible_moves, player, change_player):
    n_moves = []
    for i in len(moves):
        state_after_move = board_move(moves[i])
        n_moves_p1 = get_all_posible_moves(state_after_move, player)
        n_moves_p2 = get_all_posible_moves(state_after_move, change_player(player))
        n_moves.append(n_moves_p1 - n_moves_p2)
    index = n_moves.index(max(n_moves))
    return n_moves[index]