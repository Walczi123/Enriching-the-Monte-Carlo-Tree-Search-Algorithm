from games.hive.evaluate import hive_evaluate
from games.hex.evaluate import hex_evaluate
from games.othello.evaluate import othello_evaluate
from games.player import MCTS_Player, MCTSRAVE_Player, AlphaBeta_Player, MCTSStrategy_Player, MCTSSwitchingStrategy_Player, Strategy_Player
from strategies.hex_strategies import evaluatehex_strategy
from strategies.hive_strategies import evaluatehive_strategy, greedyhive_strategy
from strategies.othello_strategies import evaluateothello_strategy, greedyothello_strategy, mapbaseothello_strategy
from strategies.strategies import mobility_strategy, mobility_strategy_vs, random_strategy

#TESTS
SEED = 22025001
REPETITIONS = 1
RESULTS_FILE_NAME='no_such_file'


RESULTS_FILE_PATH = f'./{RESULTS_FILE_NAME}.csv'
FINISHED_RESULTS_FILE_PATH = f'./{RESULTS_FILE_NAME}_done.csv'

#MCTS
MCTS_ITERATIONS = 5

#HIVE
ROUND_LIMIT = 5
ROUND_LIMITS = [50, 100, 200, 300]

#HEX
BOARD_SIZE = 11

# TESTS
COMMON_PLAYERS = [
                #MCTS
                MCTS_Player(number_of_iteration=1000), 
                MCTS_Player(number_of_iteration=2000),
                MCTS_Player(number_of_iteration=5000), 
                MCTS_Player(number_of_iteration=10000),
                #MCTS RAVE
                MCTSRAVE_Player(number_of_iteration=1000), 
                MCTSRAVE_Player(number_of_iteration=2000),
                MCTSRAVE_Player(number_of_iteration=5000),
                MCTSRAVE_Player(number_of_iteration=10000),
                #STRATEGY
                Strategy_Player(random_strategy),
                Strategy_Player(mobility_strategy_vs),
                Strategy_Player(mobility_strategy),
                #MCST STRATEGY
                MCTSStrategy_Player(mobility_strategy_vs, number_of_iteration=1000),
                MCTSStrategy_Player(mobility_strategy_vs, number_of_iteration=2000),
                MCTSStrategy_Player(mobility_strategy_vs, number_of_iteration=5000),
                MCTSStrategy_Player(mobility_strategy_vs, number_of_iteration=10000),
                
                MCTSStrategy_Player(mobility_strategy, number_of_iteration=1000),
                MCTSStrategy_Player(mobility_strategy, number_of_iteration=2000),
                MCTSStrategy_Player(mobility_strategy, number_of_iteration=5000),
                MCTSStrategy_Player(mobility_strategy, number_of_iteration=10000)    
                ]

HIVE_PLAYERS = [
                #ALPHA BETA
                AlphaBeta_Player(hive_evaluate, 4), 
                # AlphaBeta_Player(hive_evaluate, 6), 
                # AlphaBeta_Player(hive_evaluate, 8), 
                # AlphaBeta_Player(hive_evaluate, 10),
                #STRATEGY
                Strategy_Player(evaluatehive_strategy),
                Strategy_Player(greedyhive_strategy),
                #MCST STRATEGY
                MCTSStrategy_Player(evaluatehive_strategy, number_of_iteration=1000),
                # MCTSStrategy_Player(evaluatehive_strategy, number_of_iteration=2000),
                # MCTSStrategy_Player(evaluatehive_strategy, number_of_iteration=5000),
                # MCTSStrategy_Player(evaluatehive_strategy, number_of_iteration=10000),

                MCTSStrategy_Player(greedyhive_strategy, number_of_iteration=1000),
                # MCTSStrategy_Player(greedyhive_strategy, number_of_iteration=2000),
                # MCTSStrategy_Player(greedyhive_strategy, number_of_iteration=5000),
                # MCTSStrategy_Player(greedyhive_strategy, number_of_iteration=10000),
                #MCST SWITCHING
                MCTSSwitchingStrategy_Player([random_strategy, mobility_strategy_vs, mobility_strategy, evaluatehive_strategy, greedyhive_strategy], number_of_iteration=1000),
                # MCTSSwitchingStrategy_Player([random_strategy, mobility_strategy_vs, mobility_strategy, evaluatehive_strategy, greedyhive_strategy], number_of_iteration=2000),
                # MCTSSwitchingStrategy_Player([random_strategy, mobility_strategy_vs, mobility_strategy, evaluatehive_strategy, greedyhive_strategy], number_of_iteration=5000),
                # MCTSSwitchingStrategy_Player([random_strategy, mobility_strategy_vs, mobility_strategy, evaluatehive_strategy, greedyhive_strategy], number_of_iteration=10000)
                ]


HEX_PLAYERS = [
                #ALPHA BETA
                AlphaBeta_Player(hex_evaluate, 4), 
                # AlphaBeta_Player(hex_evaluate, 6), 
                # AlphaBeta_Player(hex_evaluate, 8), 
                # AlphaBeta_Player(hex_evaluate, 10),
                #STRATEGY
                Strategy_Player(evaluatehex_strategy),
                #MCST STRATEGY
                MCTSStrategy_Player(evaluatehex_strategy, number_of_iteration=1000),
                # MCTSStrategy_Player(evaluatehex_strategy, number_of_iteration=2000),
                # MCTSStrategy_Player(evaluatehex_strategy, number_of_iteration=5000),
                # MCTSStrategy_Player(evaluatehex_strategy, number_of_iteration=10000),

                #MCST SWITCHING
                MCTSSwitchingStrategy_Player([random_strategy, mobility_strategy_vs, mobility_strategy, evaluatehex_strategy], number_of_iteration=1000),
                # MCTSSwitchingStrategy_Player([random_strategy, mobility_strategy_vs, mobility_strategy, evaluatehex_strategy], number_of_iteration=2000),
                # MCTSSwitchingStrategy_Player([random_strategy, mobility_strategy_vs, mobility_strategy, evaluatehex_strategy], number_of_iteration=5000),
                # MCTSSwitchingStrategy_Player([random_strategy, mobility_strategy_vs, mobility_strategy, evaluatehex_strategy], number_of_iteration=10000)
                ]

OTHELLO_PLAYERS = [
                #ALPHA BETA
                AlphaBeta_Player(othello_evaluate, 4), 
                AlphaBeta_Player(othello_evaluate, 6),
                AlphaBeta_Player(othello_evaluate, 8), 
                AlphaBeta_Player(othello_evaluate, 10),
                #STRATEGY
                Strategy_Player(mapbaseothello_strategy),
                Strategy_Player(greedyothello_strategy),
                Strategy_Player(evaluateothello_strategy),
                #MCST STRATEGY
                MCTSStrategy_Player(mapbaseothello_strategy, number_of_iteration=1000),
                MCTSStrategy_Player(mapbaseothello_strategy, number_of_iteration=2000),
                MCTSStrategy_Player(mapbaseothello_strategy, number_of_iteration=5000),
                MCTSStrategy_Player(mapbaseothello_strategy, number_of_iteration=10000),  

                MCTSStrategy_Player(greedyothello_strategy, number_of_iteration=1000),
                MCTSStrategy_Player(greedyothello_strategy, number_of_iteration=2000),
                MCTSStrategy_Player(greedyothello_strategy, number_of_iteration=5000),
                MCTSStrategy_Player(greedyothello_strategy, number_of_iteration=10000), 

                MCTSStrategy_Player(evaluateothello_strategy, number_of_iteration=1000),
                MCTSStrategy_Player(evaluateothello_strategy, number_of_iteration=2000),
                MCTSStrategy_Player(evaluateothello_strategy, number_of_iteration=5000),
                MCTSStrategy_Player(evaluateothello_strategy, number_of_iteration=10000), 
                #MCST SWITCHING
                MCTSSwitchingStrategy_Player([random_strategy, mobility_strategy_vs, mobility_strategy, mapbaseothello_strategy, greedyothello_strategy, evaluateothello_strategy], number_of_iteration=1000),
                MCTSSwitchingStrategy_Player([random_strategy, mobility_strategy_vs, mobility_strategy, mapbaseothello_strategy, greedyothello_strategy, evaluateothello_strategy], number_of_iteration=2000),
                MCTSSwitchingStrategy_Player([random_strategy, mobility_strategy_vs, mobility_strategy, mapbaseothello_strategy, greedyothello_strategy, evaluateothello_strategy], number_of_iteration=5000),
                MCTSSwitchingStrategy_Player([random_strategy, mobility_strategy_vs, mobility_strategy, mapbaseothello_strategy, greedyothello_strategy, evaluateothello_strategy], number_of_iteration=10000)
                ]

#ab 4 - 6 - 8 -10
#mcts 1000 - 2000 5000 - 10 000
# mcst - mctsstrat - strat
# hive - depht - 50 - 100 - 200 - 300
