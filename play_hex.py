import os
import random
from games.hex.common import get_dijkstra_score
from games.hex.evaluate import hex_evaluate
from games.hex.hex_player import Man_Player

from games.player import AlphaBeta_Player, MCTSRAVE_Player, MCTS_Player, Random_Player, MCTSStrategy_Player, MCTSSwitchingStrategy_Player, Strategy_Player
from strategies.hex_strategies import evaluatehex_strategy
from strategies.strategies import mobility_strategy, mobility_strategy_vs, random_strategy


from games.hex.hex import Hex

if __name__ == "__main__":
    random.seed(10)
    BOARD_SIZE = 7

    # pygame.init()
    # pygame.display.set_caption("Hex")

    # p2 = Man_Player()
    # p1 = MCTS_Player(ITERMAX)
    # p2 = MCTS_Player(ITERMAX)
    # p1 = MCTS_Player(ITERMAX)
    # p2 = MCTSRAVE_Player(ITERMAX)
    # p1 = MCTSSwitchingStrategy_Player([mobility_strategy_vs, random_strategy])
    # p2 = MCTSSwitchingStrategy_Player([mobility_strategy_vs, random_strategy])
    p1 = Strategy_Player(evaluatehex_strategy)
    p2 = Strategy_Player(evaluatehex_strategy)
    # p1 = Man_Player()
    # p2 = Man_Player()

    game = Hex(board_size=BOARD_SIZE, use_ui=True, player1=p1, player2=p2)
    print(game.play())
