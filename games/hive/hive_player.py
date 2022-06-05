# from mcts import MCTS
from math import inf


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