
from games.othello.othello import Othello
from games.othello.othello_player import Greedy_Othello_Player, MapBaseHeu_Othello_Player
from games.player import AlphaBeta_Player, MCTSRAVE_Player, MCTS_Player, Random_Player, MCTSStrategy_Player, MCTSSwitchingStrategy_Player
from ai.minmax import othello_evaluate
from strategies.strategies import mobility_strategy, mobility_strategy_vs, random_strategy

if __name__ == "__main__":
    p1 = MCTSStrategy_Player(random_strategy)
    p2 = MCTSSwitchingStrategy_Player([random_strategy, mobility_strategy])

    game = Othello(use_ui=True, player1=p1, player2=p2)
    game.play()
