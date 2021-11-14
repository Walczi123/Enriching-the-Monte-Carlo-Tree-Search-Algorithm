class BaseGame():
    def __init__(self, first_player, second_player, use_gui):
        self.announcement = 'Don\'t use base class.'
        self.name = "Base Game Class"
        self.use_gui = use_gui

    def start(self):
        print(f'{self.name} starts')
        current_player = self.first_player
        while not self.endCondition():
            move = current_player.make_move()
            self.animate(move)
            self.swich_player()


