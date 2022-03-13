import random
from time import sleep

from games.othello.common import get_pieces_to_reverse
from games.player import Player

class Greedy_Othello_Player(Player):
    def __init__(self, wait_time = 0.1):
        super().__init__(False)
        self.wait_time = wait_time

    def make_move(self, args):
        (initial_state, player, get_result, get_all_posible_moves, change_player, board_move) = args
        move = None
        get_points = 0
        for m in get_all_posible_moves(initial_state, player):
            x, y = m
            p = len(get_pieces_to_reverse(initial_state, player, x, y))
            if p > get_points:
                move = m
                get_points = p
        sleep(self.wait_time)
        return move

class MapBaseHeu_Othello_Player(Player):
    def __init__(self, wait_time = 0.1):
        super().__init__(False)
        self.wait_time = wait_time

    def make_move(self, args):
        (initial_state, player, get_result, get_all_posible_moves, change_player, board_move) = args

        usefull = [[],[],[],[],[],[]]
        for x,y in get_all_posible_moves(initial_state, player):
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

        sleep(self.wait_time)
        return move
