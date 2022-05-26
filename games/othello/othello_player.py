import random

from games.othello.common import get_pieces_to_reverse
from games.player import Player
from strategies.othello_strategies import mapbaseothello_strategy

class Greedy_Othello_Player(Player):
    def __init__(self, wait_time = 0):
        super().__init__(False)
        self.wait_time = wait_time
        self.name = "greedy"

    def make_move(self, args):
        (initial_state, player, get_result, get_all_posible_moves, change_player, board_move, all_posible_moves) = args
        if not all_posible_moves:
            all_posible_moves =  get_all_posible_moves(initial_state, player)   
        move = None
        get_points = 0
        for m in all_posible_moves:
            x, y = m
            p = len(get_pieces_to_reverse(initial_state, player, x, y))
            if p > get_points:
                move = m
                get_points = p
        return move

class MapBaseHeu_Othello_Player(Player):
    def __init__(self, wait_time = 0):
        super().__init__(False)
        self.wait_time = wait_time
        self.name = "mapbaseheuothello"

    def make_move(self, args):
        (initial_state, player, get_result, get_all_posible_moves, change_player, board_move, all_posible_moves) = args
        if not all_posible_moves:
            all_posible_moves =  get_all_posible_moves(initial_state, player)   
        return mapbaseothello_strategy(all_posible_moves, board_move, get_all_posible_moves, player, change_player)
