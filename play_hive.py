import random
from config import MCTS_ITERATIONS, ROUND_LIMIT
from games.hive.hive import Hive
from games.hive.evaluate import hive_evaluate
from games.hive.hive_player import Man_Player
from games.player import AlphaBeta_Player, MCTSRAVE_Player, MCTS_Player, Random_Player, MCTSStrategy_Player, MCTSSwitchingStrategy_Player, Strategy_Player
from strategies.hive_strategies import greedyhive_strategy
from strategies.strategies import mobility_strategy, mobility_strategy_vs, random_strategy
import time

if __name__ == "__main__":
    #test_hive50_random_strategy_alphabeta4_22025001
    random.seed(2202500123)
    p1 = Random_Player()
    p2 = Random_Player()
    # p2 = Man_Player()
    game = Hive(use_ui=False, player1= p1, player2=p2, round_limit=5)

    start_time = time.time()

    print(game.play())

    print("--- %s seconds ---" % (time.time() - start_time))

