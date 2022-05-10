import random
from config import MCTS_ITERATIONS, ROUND_LIMIT
from games.hive.hive import Hive
from games.hive.evaluate import hive_evaluate
from games.hive.hive_player import Man_Player
from games.player import AlphaBeta_Player, MCTSRAVE_Player, MCTS_Player, Random_Player, MCTSStrategy_Player, MCTSSwitchingStrategy_Player
from strategies.strategies import mobility_strategy, mobility_strategy_vs, random_strategy
import time

if __name__ == "__main__":
    random.seed(456)
    p1 = MCTS_Player()
    p2 = MCTS_Player()
    game = Hive(use_ui=True, player1= p1, player2=p2, round_limit=50)
    
    start_time = time.time()

    print(game.play())

    print("--- %s seconds ---" % (time.time() - start_time))

