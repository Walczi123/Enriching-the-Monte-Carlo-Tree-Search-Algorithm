from games.hive.common_functions import find_pieces_around
from games.hive.pieces import Queen

def hive_evaluate(state, player):
    player_queen = [k for k in state.board.keys() if isinstance(state.board[k][-1], Queen) and 2 - state.board[k][-1].color[0]//128 == player]
    oponent_queen = [k for k in state.board.keys() if isinstance(state.board[k][-1], Queen) and 2 - state.board[k][-1].color[0]//128 == player%2+1]
    player_score = 0
    oponent_score = 0
    if player_queen:
        player_score = len(find_pieces_around(state, player_queen[0]))
    if oponent_score:
        oponent_score = len(find_pieces_around(state, oponent_queen[0]))
    if player_score == 6 :
        player_score = 100
    if oponent_score == 6 :
        oponent_score = 100
    return oponent_score - player_score