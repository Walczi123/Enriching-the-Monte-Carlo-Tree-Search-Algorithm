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