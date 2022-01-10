from math import inf
from typing import Callable
from mcts.mcts import mcts
from mcts.mcts_rave import mcts_rave
from mcts.minmax import minmax

class Player():
    def __init__(self, is_man):
        self.is_man = is_man

    def make_move(self, args):
        pass

class MCTS_Player(Player):
    def __init__(self, number_of_iteration:int = 100):
        super().__init__(False)
        self.number_of_iteration = number_of_iteration

    def make_move(self, args):
        (initial_state, player, get_result, get_all_posible_moves, change_player, board_move) = args
        move = mcts(initial_state, player, self.number_of_iteration, get_result, get_all_posible_moves, change_player, board_move)
        return move

class MCTSRAVE_Player(Player):
    def __init__(self, number_of_iteration:int = 100):
        super().__init__(False)
        self.number_of_iteration = number_of_iteration

    def make_move(self, args):
        (initial_state, player, get_result, get_all_posible_moves, change_player, board_move) = args
        move = mcts_rave(initial_state, player, self.number_of_iteration, get_result, get_all_posible_moves, change_player, board_move)
        return move       

class AlphaBeta_Player(Player):
    def __init__(self, evaluate:Callable, depth:int = 3):
        super().__init__(False)
        self.evaluate = evaluate
        self.depth = depth

    def make_move(self, args):
        (initial_state, player, get_result, get_all_posible_moves, change_player, board_move) = args
        move, _, _ = minmax(initial_state, player, player, 3, -inf, inf, get_all_posible_moves, board_move, get_result, change_player, self.evaluate)
        return move