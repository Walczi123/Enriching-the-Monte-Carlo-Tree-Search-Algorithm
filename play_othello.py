
import random
import time
from ai.switching_mechanism import SwitchingMechanism
from games.othello.evaluate import othello_evaluate
from games.othello.othello import Othello
from games.othello.othello_player import Greedy_Othello_Player, MapBaseHeu_Othello_Player
from games.player import AlphaBeta_Player, MCTSRAVE_Player, MCTS_Player, Man_Player, Random_Player, MCTSStrategy_Player, MCTSSwitchingStrategy_Player, Strategy_Player
from strategies.othello_strategies import evaluateothello_strategy, greedyothello_strategy, mapbaseothello_strategy
from strategies.strategies import mobility_strategy, mobility_strategy_vs, random_strategy

if __name__ == "__main__":
    random.seed(22020111)
    start_time = time.time()
    # p1 = MCTSSwitchingStrategy_Player([mobility_strategy_vs,mobility_strategy,mapbaseothello_strategy], 10)
    p1 = MCTSStrategy_Player(mapbaseothello_strategy, 10)
    p2 = Strategy_Player(greedyothello_strategy)
    # p1 = Man_Player()
    # p2 = Man_Player()

    game = Othello(use_ui=False, player1=p1, player2=p2)
    print(game.play())
    print("--- %s seconds ---" % (time.time() - start_time))
    print(p1.stats1)
    print(len(p1.stats1))
    print('-----------------')
    print(p2.stats2)
    print(len(p2.stats2))
