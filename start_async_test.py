import argparse
import multiprocessing
import re
from cv2 import dft
import pandas as pd
import random
import time
import itertools
import tqdm
from config import COMMON_PLAYERS, HEX_PLAYERS, HIVE_PLAYERS, OTHELLO_PLAYERS, REPETITIONS, RESULTS_FILE_PATH, ROUND_LIMITS, SEED
from games.hex.hex import Hex
from games.hive.hive import Hive
from games.othello.othello import Othello
from test import Test

GAME_TYPES = [Othello, Hex, Hive]

parser = argparse.ArgumentParser(description='Script to run tests in batchs.')
parser.add_argument("--batch_size", type=int, default=0)
parser.add_argument("--batch_number", type=int, default=0)

def generate_instances(game_types): 
    result = []

    # Othello, Hex, Hive
    # game_types = [Othello, Hex, Hive]
    hive_game_counter = 0
    for r in itertools.product(game_types, COMMON_PLAYERS, COMMON_PLAYERS):
        for i in range(REPETITIONS):
            if r[0] == Hive:
                hive_game_counter += 1
                for j in ROUND_LIMITS:                  
                    result.append(Test(r[0], r[1], r[2], seed = SEED + i, game_limit=j))
            else:
                result.append(Test(r[0], r[1], r[2], seed = SEED + i))

    expeded_len = ((len(COMMON_PLAYERS) * len(COMMON_PLAYERS) * len(game_types)) * REPETITIONS) + (hive_game_counter * (len(ROUND_LIMITS)-1))
    assert len(result) == expeded_len, f'Incorrect amount of test cases ({len(result)} != {expeded_len})'

    return remove_done_tests(result)

def generate_specific_instances_hex(): 
    result = []
    
    for r in itertools.product(COMMON_PLAYERS, HEX_PLAYERS):
        for i in range(REPETITIONS):
            result.append(Test(Hex, r[0], r[1], seed = SEED + i))
            result.append(Test(Hex, r[1], r[0], seed = SEED + i))
    
    for r in itertools.product(HEX_PLAYERS, HEX_PLAYERS):
        for i in range(REPETITIONS):
            result.append(Test(Hex, r[0], r[1], seed = SEED + i))


    expeded_len = ((len(COMMON_PLAYERS) * len(HEX_PLAYERS) * 2) + (len(HEX_PLAYERS) * len(HEX_PLAYERS))) * REPETITIONS
    assert len(result) == expeded_len, f'Incorrect amount of hex test cases ({len(result)} != {expeded_len})'

    return remove_done_tests(result)

def generate_specific_instances_hive(): 
    result = []
    
    for r in itertools.product(COMMON_PLAYERS, HIVE_PLAYERS, ROUND_LIMITS):
        for i in range(REPETITIONS):
            result.append(Test(Hive, r[0], r[1], seed = SEED + i, game_limit=r[2]))
            result.append(Test(Hive, r[1], r[0], seed = SEED + i, game_limit=r[2]))

    for r in itertools.product(HIVE_PLAYERS, HIVE_PLAYERS, ROUND_LIMITS):
        for i in range(REPETITIONS):
            result.append(Test(Hive, r[0], r[1], seed = SEED + i, game_limit=r[2]))


    expeded_len = ((len(COMMON_PLAYERS) * len(HIVE_PLAYERS) * 2 * len(ROUND_LIMITS)) + (len(HIVE_PLAYERS) * len(HIVE_PLAYERS) * len(ROUND_LIMITS))) * REPETITIONS
    assert len(result) == expeded_len, f'Incorrect amount of hive test cases ({len(result)} != {expeded_len})'

    return remove_done_tests(result)

def generate_specific_instances_othello(): 
    result = []
    
    for r in itertools.product(COMMON_PLAYERS, OTHELLO_PLAYERS):
        for i in range(REPETITIONS):
            result.append(Test(Othello, r[0], r[1], seed = SEED + i))
            result.append(Test(Othello, r[1], r[0], seed = SEED + i))

    for r in itertools.product(OTHELLO_PLAYERS, OTHELLO_PLAYERS):
        for i in range(REPETITIONS):
            result.append(Test(Othello, r[0], r[1], seed = SEED + i))

    expeded_len = ((len(COMMON_PLAYERS) * len(OTHELLO_PLAYERS) * 2) + (len(OTHELLO_PLAYERS) * len(OTHELLO_PLAYERS))) * REPETITIONS
    assert len(result) == expeded_len, f'Incorrect amount of othello test cases ({len(result)} != {expeded_len})'

    return remove_done_tests(result)

def remove_done_tests(iterable):
    df = pd.read_csv(RESULTS_FILE_PATH, sep=",")
    return [i for i in iterable if not i.is_in_data_frame(df)]

def take_batch(iterable, batch_size, batch_number):
    if batch_size>0 and batch_number>0:
        batches = [iterable[i:i + batch_size] for i in range(0, len(iterable), batch_size)] 
        if len(batches) < batch_number:
            print(f"Max batch_number:{len(batches)}")
            return None
        return batches[batch_number]
    return iterable

def run_test(test):
    print(f'start of {test.name}')
    test.start()

def run_tests():
    iterable = generate_instances(GAME_TYPES)
    iterable += generate_specific_instances_othello()
    iterable += generate_specific_instances_hex()
    iterable += generate_specific_instances_hive()

    print(f"batch size: {batch_size}, batch number: {batch_number}")
    iterable = take_batch(iterable, batch_size, batch_number)
    if iterable == None:
        print("nothing to test")
        return

    start_time = time.time()

    # # run_test(iterable[0])

    max_cpu = multiprocessing.cpu_count()
    p = multiprocessing.Pool(int(max_cpu))
    for _ in tqdm.tqdm(p.imap_unordered(run_test, iterable), total=len(iterable)):
        pass
    # p.map_async(run_test, iterable)
    p.close()
    p.join()

    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    args = parser.parse_args()

    batch_size = args.batch_size
    batch_number = args.batch_number
    run_tests(batch_size, batch_number)
