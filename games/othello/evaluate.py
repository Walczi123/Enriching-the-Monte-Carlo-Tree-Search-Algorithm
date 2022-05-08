def othello_evaluate(state, player):
    player1_score = 0
    player2_score = 0
    for x in range(8):
        for y in range(8):  
            if state[x][y] == 1 :
                player1_score += 1
            elif state[x][y] == 2:
                player2_score += 1
    
    return player1_score - player2_score if player == 1 else player2_score - player1_score
