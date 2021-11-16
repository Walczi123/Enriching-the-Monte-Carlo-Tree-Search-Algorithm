from mcts import MCTS


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

class MCTS_Player(Player):
    def __init__(self):
        super().__init__(False)

    def make_move(self, args):
        (logic, ui, logger, starting_player, itermax, verbose, show_predictions) = args
        mcts = MCTS(logic=logic, ui=ui, board_state=logger, starting_player=starting_player)
        return mcts.start(itermax=itermax, verbose=verbose, show_predictions=show_predictions)