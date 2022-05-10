import random

from games.hex.evaluate import hex_evaluate
     
def evaluatehex_strategy(moves, state, board_move, get_all_posible_moves, player, change_player):
    n_moves = []
    for i in range(len(moves)):
        state_after_move = board_move(state, moves[i], player)
        n_moves.append(hex_evaluate(state_after_move, player))
    index = n_moves.index(max(n_moves))
    return moves[index]