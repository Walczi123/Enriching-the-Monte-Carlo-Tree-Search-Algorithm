import os
import random
from games.hex.common import get_dijkstra_score

from games.player import AlphaBeta_Player, MCTSRAVE_Player, MCTS_Player, Random_Player, MCTSStrategy_Player, MCTSSwitchingStrategy_Player
from ai.minmax import hex_evaluate
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
    p1 = MCTSSwitchingStrategy_Player([mobility_strategy_vs, random_strategy])
    p2 = MCTSSwitchingStrategy_Player([mobility_strategy_vs, random_strategy])

    game = Hex(board_size=BOARD_SIZE, use_ui=True, player1=p1, player2=p2)
    print(game.play())
