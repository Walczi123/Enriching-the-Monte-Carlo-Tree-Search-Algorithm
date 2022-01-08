# from mcts import MCTS
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
        (ui, node) = args
        if ui is None:
            coordinates = input("Type")
            return coordinates
        else:
            return ui.get_true_coordinates(node)
