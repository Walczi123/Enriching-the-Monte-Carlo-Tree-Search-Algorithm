
from games.othello.othello import Othello
from games.othello.othello_player import Greedy_Othello_Player, MapBaseHeu_Othello_Player
from games.player import AlphaBeta_Player, MCTSRAVE_Player, MCTS_Player, Man_Player, Random_Player, MCTSStrategy_Player, MCTSSwitchingStrategy_Player, Strategy_Player
from strategies.othello_strategies import mapbaseothello_strategy
from strategies.strategies import mobility_strategy, mobility_strategy_vs, random_strategy

if __name__ == "__main__":
    p1 = Man_Player()
    # p2 = Strategy_Player(mapbaseothello_strategy)
    p2 = MCTS_Player(1000)

    game = Othello(use_ui=True, player1=p2, player2=p1)
    game.play()
