
import random
import time
from games.othello.evaluate import othello_evaluate
from games.othello.othello import Othello
from games.othello.othello_player import Greedy_Othello_Player, MapBaseHeu_Othello_Player
from games.player import AlphaBeta_Player, MCTSRAVE_Player, MCTS_Player, Man_Player, Random_Player, MCTSStrategy_Player, MCTSSwitchingStrategy_Player, Strategy_Player
from strategies.othello_strategies import mapbaseothello_strategy
from strategies.strategies import mobility_strategy, mobility_strategy_vs, random_strategy

if __name__ == "__main__":
    random.seed(22025005)
    start_time = time.time()
    p1 = AlphaBeta_Player(othello_evaluate, 4)
    # p2 = Strategy_Player(mapbaseothello_strategy)
    p2 = MCTS_Player(10)

    game = Othello(use_ui=False, player1=p1, player2=p2)
    print(game.play())
    print("--- %s seconds ---" % (time.time() - start_time))
