import multiprocessing
import time
import itertools
import tqdm
import numpy as np

from games.hex.hex import Hex
from games.othello.othello import Othello
from games.player import MCTS_Player, MCTSRAVE_Player
from games.othello.othello_player import MapBaseHeu_Othello_Player
from tests import Tests

SEED = 22021070
REPETITIONS = 5

def generate_instances():
    result = []

    player_types = [MapBaseHeu_Othello_Player]

    game_types = [Othello]
    
    for r in itertools.product(game_types, player_types, player_types):
        result.append(Tests(r[0], r[1], r[2], n_repetition = REPETITIONS, seed = SEED))

    expeded_len = (len(player_types) * len(player_types) * len(game_types))
    assert len(result) == expeded_len, f'Incorrect amount of test cases ({len(result)} != {expeded_len})'

    return result


def run_test(test):
    print(f'start of {test.name}')
    test.start()


def run_tests():
    iterable = generate_instances()
    

    start_time = time.time()

    run_test(iterable[0])

    # max_cpu = multiprocessing.cpu_count()
    # p = multiprocessing.Pool(int(max_cpu)-2)
    # for _ in tqdm.tqdm(p.imap_unordered(run_test, iterable), total=len(iterable)):
    #     pass
    # p.map_async(run_test, iterable)

    # p.close()
    # p.join()

    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    run_tests()
