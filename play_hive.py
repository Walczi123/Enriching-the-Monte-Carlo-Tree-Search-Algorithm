import random
from games.hive.hive import Hive
from games.hive.hive_player import Man_Player, MinMax_Player
from games.player import AlphaBeta_Player, MCTSRAVE_Player, MCTS_Player, Random_Player, MCTSStrategy_Player, MCTSSwitchingStrategy_Player
# from ai.minmax import hive_evaluate
from strategies.strategies import mobility_strategy, mobility_strategy_vs, random_strategy

if __name__ == "__main__":
    random.seed(1)
    p1 = MCTSRAVE_Player(max_depth=3)
    p2 = MCTS_Player(max_depth=3)
    game = Hive(use_ui=True, player1= p1, player2=p2, round_limit=10)
    game.play()

