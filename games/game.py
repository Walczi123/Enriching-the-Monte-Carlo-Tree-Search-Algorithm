from games.player import Player


class Game():
    def __init__(self, player1:Player , player2:Player , use_ui:bool = False):
        self.announcement = 'Don\'t use base class.'
        self.name = "Base Game Class"
        self.use_ui = use_ui
        self.player1 = player1
        self.player2 = player2

    def play_with_ui(self):
        raise ValueError(self.announcement)

    def play_without_ui(self):
        raise ValueError(self.announcement)

    def play(self):
        # print(f'{self.name} starts')
        if self.use_ui:
            return self.play_with_ui()
        else:
            return self.play_without_ui()

    def get_result(self, state, player) -> int:
        raise ValueError(self.announcement)

    def get_all_posible_moves(self, iteration_state, player) -> list:
        raise ValueError(self.announcement)

    def change_player(self, player) -> int:
        raise ValueError(self.announcement)

    def board_move(self, state, move, player):
        raise ValueError(self.announcement)