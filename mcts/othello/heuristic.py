import games.othello.msi2.othello2 as Game
import random


def heu(initialState, player, l):
    possibleMoves = Game.get_all_posible_moves(initialState, player)
    usefull = [[],[],[],[],[],[]]
    for x,y in possibleMoves:
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
            return random.choice(usefull[i])
        
