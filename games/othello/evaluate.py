
from games.othello.othello import get_all_posible_moves


def othello_evaluate(state, player):
    first_pos_moves = get_all_posible_moves(state, 1)
    second_pos_moves = get_all_posible_moves(state, 2)
    player1_score = 0
    player2_score = 0
    for x in range(8):
        for y in range(8):  
            if state[x][y] == 1 :
                player1_score += 1
            elif state[x][y] == 2:
                player2_score += 1
    
    if not first_pos_moves and not second_pos_moves:
        if player1_score > player2_score :
            player1_score += 100
        else :
            player2_score += 100

    return player1_score - player2_score if player == 1 else player2_score - player1_score
