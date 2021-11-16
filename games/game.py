class BaseGame():
    def __init__(self, player1, player2, use_gui):
        self.announcement = 'Don\'t use base class.'
        self.name = "Base Game Class"
        self.use_gui = use_gui
        self.player1 = player1
        self.player2 = player2

    def play_with_ui(self):
        raise ValueError(self.announcement)

    def play_without_ui(self):
        raise ValueError(self.announcement)

    def play(self):
        print(f'{self.name} starts')
        if self.use_gui:
            self.play_with_ui()
        else:
            self.play_without_ui()

    def get_result(self, state, player) -> int:
        raise ValueError(self.announcement)

    def get_all_posible_moves(self, iteration_state, player) -> list:
        raise ValueError(self.announcement)

    def change_player(self, player) -> int:
        raise ValueError(self.announcement)

    def board_move(self, state, move, player):
        raise ValueError(self.announcement)