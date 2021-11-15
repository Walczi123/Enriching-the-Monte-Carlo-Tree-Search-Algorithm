class Othello():
    def __init__(self, use_ui):
        self.name = "Othello"
        self.use_ui = use_ui

    def play_with_ui(self):
        pass

    def play_without_ui(self):
        pass

    def play(self):
        if self.use_ui:
            self.play_with_ui()
        else:
            self.play_without_ui

