# from mcts import MCTS
import random
from time import sleep
from games.hive.move_checker import check_move
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
            move = random.choice(available_moves)
            sleep(self.wait_time)
            return move
        return None