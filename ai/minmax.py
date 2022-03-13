from math import inf


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

def hex_evaluate(state, player):
    player1_score = 0
    player2_score = 0
    for x in range(8):
        for y in range(8):  
            if state[x][y] == 1 :
                player1_score += 1
            elif state[x][y] == 2:
                player2_score += 1
    
    return player1_score - player2_score if player == 1 else player2_score - player1_score

def alpha_beta_minmax(iteration_state, player, current_player, d: int, alpha: int, beta: int, get_all_posible_moves, board_move, get_result, change_player, evaluate):
    if d <= 0:
        return None, evaluate(iteration_state, player), 1

    if not get_all_posible_moves(iteration_state, player) and not get_all_posible_moves(iteration_state, change_player(player)):
        winner = get_result(iteration_state, player)
        return None, 1 if winner == player else -1, 1

    maximizing = current_player == player 
    f = max if maximizing else min
    evaluations = {}
    nn = 0
    moves = get_all_posible_moves(iteration_state, current_player)
    for move in moves:
        new_state = board_move(iteration_state, move, current_player)
        _, e, n = alpha_beta_minmax(new_state, player, change_player(current_player), d - 1, alpha, beta, get_all_posible_moves, board_move, get_result, change_player, evaluate)
        if maximizing:
            alpha = f(alpha, e)
        else:
            beta = f(beta, e)
        evaluations[move] = e
        nn += n
        if beta <= alpha:
            break

    if not evaluations:
        if maximizing:
            return None, -inf, 1 
        else:
            return None, inf, 1 
    best = f(evaluations, key=evaluations.get)
    return best, evaluations[best], nn