import os
import random
import time
from games.hex.common import get_dijkstra_score
from games.hex.evaluate import hex_evaluate
from games.hex.hex_player import Man_Player

from games.player import AlphaBeta_Player, MCTSRAVE_Player, MCTS_Player, Random_Player, MCTSStrategy_Player, MCTSSwitchingStrategy_Player, Strategy_Player
from strategies.hex_strategies import evaluatehex_strategy
from strategies.strategies import mobility_strategy, mobility_strategy_vs, random_strategy


from games.hex.hex import Hex

if __name__ == "__main__":
    # random.seed(22025002)
    BOARD_SIZE = 7
    
    p1 = MCTS_Player(3)
    p2 = MCTS_Player(3)

    game = Hex(board_size=BOARD_SIZE, use_ui=False, player1=p1, player2=p2)
    start_time = time.time()

    print(game.play())

    print("--- %s seconds ---" % (time.time() - start_time))
