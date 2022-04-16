import multiprocessing
import time
import itertools
from ai.minmax import othello_evaluate
import tqdm
import numpy as np

from games.hex.hex import Hex
from games.othello.othello import Othello
from games.player import MCTS_Player, MCTSRAVE_Player, Random_Player, AlphaBeta_Player
from games.othello.othello_player import MapBaseHeu_Othello_Player, Greedy_Othello_Player
from test import Test

SEED = 22021070
REPETITIONS = 5

def generate_instances(): 
    result = []

    player_types = [MCTS_Player(), MCTSRAVE_Player(), MapBaseHeu_Othello_Player(), Greedy_Othello_Player(), Random_Player(), AlphaBeta_Player(othello_evaluate)]

    game_types = [Othello]
    
    for r in itertools.product(game_types, player_types, player_types):
        for i in range(REPETITIONS):
            result.append(Test(r[0], r[1], r[2], seed = SEED + i))

    expeded_len = (len(player_types) * len(player_types) * len(game_types)) * REPETITIONS
    assert len(result) == expeded_len, f'Incorrect amount of test cases ({len(result)} != {expeded_len})'

    return result


def run_test(test):
    print(f'start of {test.name}')
    test.start()


def run_tests():
    iterable = generate_instances()
    print(len(iterable))

    start_time = time.time()

    # run_test(iterable[0])

    max_cpu = multiprocessing.cpu_count()
    p = multiprocessing.Pool(int(max_cpu)-2)
    for _ in tqdm.tqdm(p.imap_unordered(run_test, iterable), total=len(iterable)):
        pass
    # p.map_async(run_test, iterable)
    p.close()
    p.join()

    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    run_tests()
