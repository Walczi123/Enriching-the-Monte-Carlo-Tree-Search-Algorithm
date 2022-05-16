import random
from games.hive.common_functions import neighbours

from games.hive.evaluate import hive_evaluate
from games.hive.pieces import Queen
     
def evaluatehive_strategy(moves, state, board_move, get_all_posible_moves, player, change_player):
    n_moves = []
    for i in range(len(moves)):
        state_after_move = board_move(state, moves[i], player)
        n_moves.append(hive_evaluate(state_after_move, player))
    index = n_moves.index(max(n_moves))
    return moves[index]

def greedyhive_strategy(moves, state, board_move, get_all_posible_moves, player, change_player):
    oponent_queen_coordinates = [k for k in state.board.keys() if isinstance(state.board[k][-1], Queen) and 2 - state.board[k][-1].color[0]//128 == player%2+1]
    n_moves = []
    if oponent_queen_coordinates:
        oponent_queen_neighbours = neighbours(oponent_queen_coordinates[0])
        for m in moves:
            if not m[0][0] and not m[0][1] in oponent_queen_neighbours and m[1] in oponent_queen_neighbours:
                n_moves.append(m)
        if n_moves:
            return random.choice(n_moves)
    return random.choice(moves)