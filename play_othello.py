
from games.othello.othello import Othello
from games.player import AlphaBeta_Player, MCTSRAVE_Player, MCTS_Player
from mcts.minmax import othello_evaluate

if __name__ == "__main__":
    p1 = MCTSRAVE_Player(10)
    # p2 = Random_Player()
    p2 = AlphaBeta_Player(othello_evaluate, 3)

    game = Othello(use_ui=True, player1= p1, player2=p2)
    game.play()

