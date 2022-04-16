import random
from time import sleep
from math import inf
from typing import Callable
from ai.mcts import mcts
from ai.mcts_rave import mcts_rave
from ai.mcts_strategy import mcts_strategy
from ai.minmax import alpha_beta_minmax
from strategies.strategies import random_strategy

class Player():
    def __init__(self, is_man):
        self.is_man = is_man
        self.name = "player"

    def get_name(self):
        return self.name

    def make_move(self, args):
        pass

class Man_Player(Player):
    def __init__(self):
        super().__init__(True)
        self.name = "man"

    def make_move(self, args):
        return args

class MCTS_Player(Player):
    def __init__(self, number_of_iteration:int = 100):
        super().__init__(False)
        self.name = f"mcts{str(number_of_iteration)}"
        self.number_of_iteration = number_of_iteration

    def make_move(self, args):
        (initial_state, player, get_result, get_all_posible_moves, change_player, board_move) = args
        move = mcts(initial_state, player, self.number_of_iteration, get_result, get_all_posible_moves, change_player, board_move)
        return move

class MCTSRAVE_Player(Player):
    def __init__(self, number_of_iteration:int = 100):
        super().__init__(False)
        self.number_of_iteration = number_of_iteration
        self.name = f"mctsrave{str(number_of_iteration)}"

    def make_move(self, args):
        (initial_state, player, get_result, get_all_posible_moves, change_player, board_move) = args
        move = mcts_rave(initial_state, player, self.number_of_iteration, get_result, get_all_posible_moves, change_player, board_move)
        return move       

class MCTSStrategy_Player(Player):
    def __init__(self, strategy:Callable, number_of_iteration:int = 100):
        super().__init__(False)
        self.strategy = strategy
        self.number_of_iteration = number_of_iteration
        self.name = f"mctsstrategy{str(number_of_iteration)}{self.strategy.name}"

    def make_move(self, args):
        (initial_state, player, get_result, get_all_posible_moves, change_player, board_move) = args
        move = mcts(initial_state, player, self.number_of_iteration, get_result, get_all_posible_moves, change_player, board_move, self.strategy)
        return move

class MCTSSwitchingStrategy_Player(Player):
    def __init__(self, strategies:list, number_of_iteration:int = 100):
        super().__init__(False)
        self.strategies = strategies
        self.number_of_iteration = number_of_iteration
        self.name = f"mctsstrategies{str(number_of_iteration)}{self.strateies.name}"

    def make_move(self, args):
        (initial_state, player, get_result, get_all_posible_moves, change_player, board_move) = args
        move = mcts(initial_state, player, self.number_of_iteration, get_result, get_all_posible_moves, change_player, board_move, self.strategies)
        return move

class AlphaBeta_Player(Player):
    def __init__(self, evaluate:Callable, depth:int = 3):
        super().__init__(False)
        self.evaluate = evaluate
        self.depth = depth
        self.name = f"alphabeta{str(depth)}"

    def make_move(self, args):
        (initial_state, player, get_result, get_all_posible_moves, change_player, board_move) = args
        move, _, _ = alpha_beta_minmax(initial_state, player, player, 3, -inf, inf, get_all_posible_moves, board_move, get_result, change_player, self.evaluate)
        return move

class Random_Player(Player):
    def __init__(self, wait_time = 0):
        super().__init__(False)
        self.wait_time = wait_time
        self.name = "random"

    def make_move(self, args):
        (initial_state, player, get_result, get_all_posible_moves, change_player, board_move) = args
        move = random_strategy(get_all_posible_moves(initial_state, player), board_move, get_all_posible_moves, player, change_player)
        sleep(self.wait_time)
        return move