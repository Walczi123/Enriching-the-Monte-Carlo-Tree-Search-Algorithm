import random
from config import MCTS_ITERATIONS, MCTS_MAX_DEPTH, ROUND_LIMIT
from games.hive.hive import Hive
from games.hive.hive_evaluate import hive_evaluate
from games.hive.hive_player import Man_Player, MinMax_Player
from games.player import AlphaBeta_Player, MCTSRAVE_Player, MCTS_Player, Random_Player, MCTSStrategy_Player, MCTSSwitchingStrategy_Player
from strategies.strategies import mobility_strategy, mobility_strategy_vs, random_strategy

if __name__ == "__main__":
    random.seed(22021070)
    p1 = MCTS_Player(number_of_iteration = MCTS_ITERATIONS, max_depth = MCTS_MAX_DEPTH)
    p2 = MCTS_Player(number_of_iteration = MCTS_ITERATIONS, max_depth = MCTS_MAX_DEPTH)
    game = Hive(use_ui=False, player1= p1, player2=p2, round_limit=ROUND_LIMIT)
    game.play()

