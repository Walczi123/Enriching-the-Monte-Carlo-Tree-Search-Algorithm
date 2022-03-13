
from games.othello.othello import Othello
from games.othello.othello_player import Greedy_Othello_Player, MapBaseHeu_Othello_Player
from games.player import AlphaBeta_Player, MCTSRAVE_Player, MCTS_Player, Random_Player
from ai.minmax import othello_evaluate

if __name__ == "__main__":
    # p1 = MCTSRAVE_Player(10)
    # p2 = Random_Player()
    # p1 = MapBaseHeu_Othello_Player()
    p1 = AlphaBeta_Player(othello_evaluate)
    p2 = AlphaBeta_Player(othello_evaluate)

    game = Othello(use_ui=True, player1= p1, player2=p2)
    game.play()

