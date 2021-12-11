from games.hive.hive import Hive
from games.hive.player import Player


if __name__ == "__main__":
    p1 = Player(True)
    p2 = Player(False)
    # p2 = MCTS_Player(10)

    game = Hive(use_ui=True, player1= p1, player2=p2)
    game.play()

