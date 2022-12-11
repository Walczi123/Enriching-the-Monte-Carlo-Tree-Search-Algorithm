from ast import Str
from games.hive.evaluate import hive_evaluate
from games.hex.evaluate import hex_evaluate
from games.othello.evaluate import othello_evaluate
from games.player import MCTS_Player, MCTSRAVE_Player, AlphaBeta_Player, MCTSRAVEv2_Player, MCTSStrategy_Player, MCTSSwitchingStrategy_Player, Strategy_Player
from strategies.hex_strategies import evaluatehex_strategy
from strategies.hive_strategies import evaluatehive_strategy, greedyhive_strategy
from strategies.othello_strategies import evaluateothello_strategy, greedyothello_strategy, mapbaseothello_strategy
from strategies.strategies import mobility_strategy, mobility_strategy_vs, random_strategy

#TESTS
SEED = 22020110
REPETITIONS = 1
RESULTS_FILE_NAME='hive10_part_tests'


RESULTS_FILE_PATH = f'./{RESULTS_FILE_NAME}.csv'
FINISHED_RESULTS_FILE_PATH = f'./{RESULTS_FILE_NAME}_done.csv'

#MCTS
MCTS_ITERATIONS = 10

#HIVE
ROUND_LIMIT = 5
ROUND_LIMITS = [10]

#HEX
BOARD_SIZE = 11

# TESTS
COMMON_PLAYERS = [
    
]

HIVE_PLAYERS = [
    MCTSStrategy_Player(mobility_strategy_vs, 500),
    MCTSStrategy_Player(evaluatehive_strategy, 500),
    MCTSStrategy_Player(greedyhive_strategy, 500),
    MCTSStrategy_Player(mobility_strategy, 500),
    
    Strategy_Player(random_strategy),
    Strategy_Player(greedyhive_strategy),
    Strategy_Player(mobility_strategy_vs),
    Strategy_Player(mobility_strategy),
    
    MCTS_Player(500),
    MCTSRAVE_Player(500),
    MCTSRAVEv2_Player(500),

    MCTSSwitchingStrategy_Player([random_strategy, mobility_strategy_vs, mobility_strategy, evaluatehive_strategy, greedyhive_strategy], number_of_iteration=500),
    MCTSSwitchingStrategy_Player([mobility_strategy_vs, mobility_strategy, evaluatehive_strategy, greedyhive_strategy], 500),

    AlphaBeta_Player(hive_evaluate, 10),
    AlphaBeta_Player(hive_evaluate, 12)
    ]


HEX_PLAYERS = [
    MCTS_Player(10000),
    MCTSSwitchingStrategy_Player([random_strategy, mobility_strategy_vs, mobility_strategy, evaluatehex_strategy], 10000),
    MCTSSwitchingStrategy_Player([mobility_strategy_vs,mobility_strategy,evaluatehex_strategy], 10000),
    AlphaBeta_Player(hex_evaluate, 10),
    MCTSStrategy_Player(mobility_strategy, 10000),
    MCTSStrategy_Player(mobility_strategy_vs, 10000),
    MCTSStrategy_Player(evaluatehex_strategy, 10000),
    Strategy_Player(evaluatehex_strategy),
    Strategy_Player(random_strategy),
    MCTSRAVE_Player(10000),
    MCTSRAVEv2_Player(10000),
    AlphaBeta_Player(hex_evaluate, 12)
    ]

OTHELLO_PLAYERS = [
    MCTSStrategy_Player(mobility_strategy_vs, 10000),
    MCTSStrategy_Player(mapbaseothello_strategy, 10000),
    MCTSStrategy_Player(mobility_strategy, 10000),
    MCTS_Player(10000),
    MCTSSwitchingStrategy_Player([random_strategy, mobility_strategy_vs,mobility_strategy,mapbaseothello_strategy,greedyothello_strategy,evaluateothello_strategy], 10000),
    MCTSRAVE_Player(10000),
    AlphaBeta_Player(othello_evaluate, 10),
    Strategy_Player(random_strategy),
    Strategy_Player(greedyothello_strategy),
    MCTSSwitchingStrategy_Player([mobility_strategy_vs,mobility_strategy,mapbaseothello_strategy], 10000),
    MCTSRAVEv2_Player(10000),
    AlphaBeta_Player(othello_evaluate, 12)
    ]
