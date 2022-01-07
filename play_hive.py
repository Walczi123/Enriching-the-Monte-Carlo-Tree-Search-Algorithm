import random
from games.hive.hive import Hive
from games.hive.player import MCTS_Player, Man_Player, MinMax_Player, Player, Random_Player


if __name__ == "__main__":
    random.seed(123)
    # p1 = Random_Player(0)
    # p2 = Random_Player(0)
    p1 = Man_Player()
    p2 = MinMax_Player(2)
    # p2 = MCTS_Player(10)

    game = Hive(use_ui=True, player1= p1, player2=p2)
    game.play()

