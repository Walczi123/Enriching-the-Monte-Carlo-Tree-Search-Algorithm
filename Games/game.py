class Game:
    def __init__(self):
        self.announcement = 'Don\'t use base class.'

    def start(self):
        raise self.announcement