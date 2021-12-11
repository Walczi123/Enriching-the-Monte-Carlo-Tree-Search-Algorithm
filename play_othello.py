from games.hex.player import MCTS_Player, Man_Player
from games.othello.othello import Othello
from games.othello.player import Man_Player, Random_Player

if __name__ == "__main__":
    p1 = Man_Player()
    p2 = Random_Player()
    # p2 = MCTS_Player(10)

    game = Othello(use_ui=True, player1= p1, player2=p2)
    game.play()

