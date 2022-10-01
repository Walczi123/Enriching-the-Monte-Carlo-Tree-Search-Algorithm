
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
    random.seed(22025005)
    start_time = time.time()
    p1 = MCTSSwitchingStrategy_Player([random_strategy, mobility_strategy_vs,mobility_strategy,mapbaseothello_strategy,greedyothello_strategy,evaluateothello_strategy], 10)
    # p2 = Strategy_Player(mapbaseothello_strategy)
    p2 = Man_Player()

    game = Othello(use_ui=True, player1=p1, player2=p2)
    print(game.play())
    print("--- %s seconds ---" % (time.time() - start_time))

#    sm = SwitchingMechanism([random_strategy, mobility_strategy_vs,mobility_strategy,mapbaseothello_strategy,greedyothello_strategy,evaluateothello_strategy])
#    sm.choose_strategy(0)
