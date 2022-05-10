import random
from games.othello.common import get_pieces_to_reverse
from games.othello.evaluate import othello_evaluate


def mapbaseothello_strategy(moves, state, board_move, get_all_posible_moves, player, change_player):
    usefull = [[],[],[],[],[]]
    for x,y in moves:
        # corner places
        if (x % 7 == 0 and y % 7 == 0):
            usefull[0].append((x,y))
        # middle square placements
        elif (x, y) in [(2, 2), (2, 3), (2, 4), (2, 5), (3, 2), (3, 5), (4, 2), (4, 5), (5, 2), (5, 3), (5, 4), (5, 5)]:
            usefull[1].append((x, y))
        # next to corners
        elif (x, y) in [(0, 1), (0, 6), (1, 0), (1, 7), (7, 1), (7, 6), (6, 0), (6, 7)]:
            usefull[3].append((x, y))
        # cross to corners
        elif (x,y) in [(1,1), (6,6), (1,6), (6,1)]:
            usefull[4].append((x, y))
        else: 
            usefull[2].append((x, y))

    for i in range(5):
        if usefull[i] != []:
            move = random.choice(usefull[i])
            break
    
    return move

def greedyothello_strategy(moves, state, board_move, get_all_posible_moves, player, change_player):
    move = None
    get_points = 0
    for m in moves:
        x, y = m
        p = len(get_pieces_to_reverse(state, player, x, y))
        if p > get_points:
            move = m
            get_points = p
    return move
       
def evaluateothello_strategy(moves, state, board_move, get_all_posible_moves, player, change_player):
    n_moves = []
    for i in range(len(moves)):
        state_after_move = board_move(state, moves[i], player)
        n_moves.append(othello_evaluate(state_after_move, player))
    index = n_moves.index(max(n_moves))
    return moves[index]