
from games.othello.othello import Othello
from games.player import MCTSRAVE_Player, MCTS_Player

if __name__ == "__main__":
    p1 = MCTSRAVE_Player(10)
    # p2 = Random_Player()
    p2 = MCTSRAVE_Player(10)

    game = Othello(use_ui=True, player1= p1, player2=p2)
    game.play()

