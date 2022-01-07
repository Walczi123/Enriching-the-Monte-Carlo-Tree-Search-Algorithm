# from mcts import MCTS
from copy import deepcopy
from math import inf
import random
import sys
from time import sleep
from games.hive.common_functions import neighbours
from games.hive.const import QUEEN_ID
from games.hive.move_checker import check_move
from games.hive.pieces import Queen
from games.hive.state import State
from mcts import mcts


class Player():
    def __init__(self, is_man):
        self.is_man = is_man

    def make_move(self, args):
        pass

class Man_Player(Player):
    def __init__(self):
        super().__init__(True)

    def make_move(self, args):
        return args

class MCTS_Player(Player):
    def __init__(self, number_of_iteration:int):
        super().__init__(False)
        self.number_of_iteration = number_of_iteration
    def make_move(self, args):
        (initial_state, player, get_result, get_all_posible_moves, change_player, board_move) = args
        move = mcts.mcts(initial_state, player, self.number_of_iteration, get_result, get_all_posible_moves, change_player, board_move)
        return move

class Random_Player(Player):
    def __init__(self, wait_time = 0.1):
        super().__init__(False)
        self.wait_time = wait_time

    def make_move(self, args):
        (initial_state, player, get_result, get_all_posible_moves, change_player, board_move) = args
        available_moves = get_all_posible_moves(initial_state)
        if len(available_moves) > 0:
            for m in available_moves:
                if not check_move(initial_state, m):
                    print("invalide move generated")
                    print(m)
                    print()
                    sys.exit()
            move = random.choice(available_moves)
            sleep(self.wait_time)
            return move
        return None

class MinMax_Player(Player):
    def __init__(self, number_of_iteration:int):
        super().__init__(False)
        self.number_of_iteration = number_of_iteration
        
    def make_move(self, args):
        (initial_state, player, get_result, get_all_posible_moves, change_player, board_move) = args
        move, _, n = minmax(initial_state, player, 3, -inf, inf, get_all_posible_moves, board_move)
        return move

def find(state, player, type):
    for c, pieces in state.board.items():
        for piece in pieces:
            if 2 - piece.color[0]//128 == player and isinstance(piece, type):
                return c
    return None

def evaluate(state, player):
    other = (player % 2) + 1

    player_queen = find(state, player, Queen)
    other_queen = find(state, other, Queen)
    player_free = len([n for n in neighbours(player_queen) if n not in state.board]) if player_queen else 0
    other_free = len([n for n in neighbours(other_queen) if n not in state.board]) if other_queen else 0
    return player_free - 2 * other_free

def is_looser(state:State, player):
        queen_coordinate = find(state, player, Queen)
        if queen_coordinate:
            if all(n in state.board.keys() for n in neighbours(queen_coordinate)):
                return True
        return False

def winner(state):
    if is_looser(state, 1):
        return 2
    if is_looser(state, 2):
        return 1
    return None

def minmax(state: State, player: Player, d: int, alpha: int, beta: int, get_all_posible_moves, board_move):
    if d <= 0:
        return None, evaluate(state, player), 1

    the_winner = winner(state)
    if the_winner:
        print("leaf!")
        return None, 1 if the_winner == player else -1, 1

    maximizing = state.turn_state == player 
    f = max if maximizing else min
    evaluations = {}
    nn = 0
    moves = get_all_posible_moves(state)
    for move in moves:
        new_state = deepcopy(state)
        board_move(state, move, player)
        _, e, n = minmax(new_state, player, d - 1, alpha, beta, get_all_posible_moves, board_move)
        if maximizing:
            alpha = f(alpha, e)
        else:
            beta = f(beta, e)
        evaluations[move] = e
        nn += n
        if beta <= alpha:
            break

    best = f(evaluations, key=evaluations.get)
    return best, evaluations[best], nn