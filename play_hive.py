import random
from games.hive.hive import Hive
from games.hive.hive_evaluate import hive_evaluate
from games.hive.hive_player import Man_Player, MinMax_Player
from games.player import AlphaBeta_Player, MCTSRAVE_Player, MCTS_Player, Random_Player, MCTSStrategy_Player, MCTSSwitchingStrategy_Player
from strategies.strategies import mobility_strategy, mobility_strategy_vs, random_strategy

if __name__ == "__main__":
    # random.seed(12)
    p1 = AlphaBeta_Player(hive_evaluate)
    p2 = AlphaBeta_Player(hive_evaluate)
    game = Hive(use_ui=True, player1= p1, player2=p2, round_limit=10)
    game.play()

