import random
from time import sleep
from math import inf
from typing import Callable
from ai.mcts import mcts
from ai.mcts_rave import mcts_rave
from ai.minmax import alpha_beta_minmax

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
        move, _, _ = alpha_beta_minmax(initial_state, player, player, 3, -inf, inf, get_all_posible_moves, board_move, get_result, change_player, self.evaluate)
        return move

class Random_Player(Player):
    def __init__(self, wait_time = 0.1):
        super().__init__(False)
        self.wait_time = wait_time

    def make_move(self, args):
        # (logic, ui, logger, starting_player, itermax, verbose, show_predictions) = args
        # mcts = MCTS(logic=logic, ui=ui, board_state=logger, starting_player=starting_player)
        # return mcts.start(itermax=itermax, verbose=verbose, show_predictions=show_predictions)
        (initial_state, player, get_result, get_all_posible_moves, change_player, board_move) = args
        move = random.choice(get_all_posible_moves(initial_state, player))
        sleep(self.wait_time)
        return move