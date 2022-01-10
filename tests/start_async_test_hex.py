import multiprocessing
import time
import itertools
import tqdm
import numpy as np
from games.hex.hex import Hex

from games.player import MCTS_Player
from tests.code.Test import Test

SEED = 22021070
REPETITIONS = 100

def layer_amount(layers):
    return str(len(layers))

def nodes_amount(layers):
    return str(int(np.sum(layers)))

def dataset_name_amount(dataset_path):
    splited = dataset_path.split('.')
    return f'{splited[1].replace("_","-")}_{splited[3]}'

def get_input_output_dataset(problem_type, dataset_path):
    if problem_type == problem_type.Regression:
        return (1,1)
    else:
        dataset = prepare_data(problem_type, dataset_path)
        len_test_inputs = len(np.unique([y for x, y in dataset]))
        return (2, len_test_inputs)

def generate_instances():
    result = []

    player_types = [MCTS_Player]

    game_types = [Hex]
    
    for r in itertools.product(player_types, player_types, game_types):
        result.append(Test(r[0], r[1], r[2], REPETITIONS, SEED))

    expeded_len = (len(player_types) * len(player_types) * len(game_types))
    assert len(result) == expeded_len, f'Incorrect amount of test cases ({len(result)} != {expeded_len})'

    return result


def run_test(test):
    print(f'start of {test.name}')
    # test.start()


def run_tests():
    iterable = generate_instances()
    # iterable[0].start()

    # start_time = time.time()

    # max_cpu = multiprocessing.cpu_count()
    # p = multiprocessing.Pool(int(max_cpu/2))
    # for _ in tqdm.tqdm(p.imap_unordered(run_test, iterable), total=len(iterable)):
    #     pass
    # p.map_async(run_test, iterable)

    # p.close()
    # p.join()

    # print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    run_tests()
