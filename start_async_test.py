import argparse
import multiprocessing
import os
import time
import itertools
import tqdm
from config import COMMON_PLAYERS, FINISHED_RESULTS_FILE_PATH, HEX_PLAYERS, HIVE_PLAYERS, OTHELLO_PLAYERS, REPETITIONS, ROUND_LIMITS, SEED
from games.game import Game
from games.hex.hex import Hex
from games.hive.hive import Hive
from games.othello.othello import Othello
from test import Test

GAME_TYPES = [Othello, Hex, Hive]

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def str2game(v):
    if isinstance(v, Game):
        return v
    if v.lower() in ('othello'):
        return Othello
    elif v.lower() in ('hex'):
        return Hex
    elif v.lower() in ('hive'):
        return Hive
    else:
        raise argparse.ArgumentTypeError('Game name expected.')

parser = argparse.ArgumentParser(description='Script to run tests in batchs.')
parser.add_argument('-bs', "--batch_size", type=int, default=0)
parser.add_argument('-bn', "--batch_number", type=int, default=0)
parser.add_argument('-g',"--game_list", type=str2game, nargs="+", default=[Othello, Hex, Hive])
parser.add_argument('-r',"--remove_done_tests", type=str2bool, nargs='?', const=True, default=True, help="Activate removing done tests.")

def generate_instances(game_types): 
    result = []

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

    return result

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

    return result

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

    return result

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

    return result

def remove_done_tests(iterable):
    if not os.path.exists(FINISHED_RESULTS_FILE_PATH):
        print('There is not file with finished tests.')
        return iterable
    done_tests = []
    with open(FINISHED_RESULTS_FILE_PATH) as file:
        for line in file:
            splited_line = line.split(",")
            done_tests.append((splited_line[0], splited_line[1], splited_line[2], splited_line[4]))
    
    return [i for i in iterable if not i.is_done(done_tests)]

def take_batch(iterable, batch_size, batch_number):
    if batch_size>0 and batch_number>0:
        batches = take_batches(iterable, batch_size) 
        if len(batches) < batch_number:
            print(f"Max batch_number:{len(batches)}")
            return None
        print("Created specific batch.")
        return batches[batch_number]
    print("Batch size of batch number is not proper.")
    return iterable

def take_batches(iterable, batch_size):
    if batch_size>0:
        batches = [iterable[i:i + batch_size] for i in range(0, len(iterable), batch_size)] 
        return batches
    return iterable

def run_test(test):
    print(f'start of {test.name}')
    test.start()

def create_tests(batch_size, batch_number, game_list, remove_done):
    print("----------------- CREATING TEST INSTANCES -----------------")
    iterable = generate_instances(game_list)
    print(f"Created {len(iterable)} test instances of common type.")
    if Othello in game_list: 
        iterable_othello = generate_specific_instances_othello()
        print(f"Created {len(iterable_othello)} specific test instances of Othello.")
        iterable += iterable_othello
    if Hex in game_list: 
        iterable_hex = generate_specific_instances_hex()
        print(f"Created {len(iterable_hex)} specific test instances of Hex.")
        iterable += iterable_hex
    if Hive in game_list: 
        iterable_hive = generate_specific_instances_hive()
        print(f"Created {len(iterable_hive)} specific test instances of Hive.")
        iterable += iterable_hive
    print("----------------- REMOVING FINISHED TESTS  -----------------")
    if remove_done: 
        print(f"All generated test amount: {len(iterable)}")
        iterable = remove_done_tests(iterable)
        print(f"After applaying removig test amount: {len(iterable)}")
    else:
        print("Removing done tests is disabled.")
    print("----------------- CREATING BATCHES OF TESTS  -----------------")
    iterable = take_batch(iterable, batch_size, batch_number)
    return iterable

def run_tests(batch_size, batch_number, game_list, remove_done):
    iterable = create_tests(batch_size, batch_number, game_list, remove_done)
    if iterable == None:
        print("Nothing to test")
        return

    print("----------------- TESTING STARTS  -----------------")
    print(f"Start batch of {len(iterable)} tests.")
    print(f"Batch size: {batch_size}, batch number: {batch_number}.")
    print(f"Test for games: {[x.__name__ for x in game_list]}")

    start_time = time.time()

    max_cpu = multiprocessing.cpu_count()
    p = multiprocessing.Pool(int(max_cpu))
    for _ in tqdm.tqdm(p.imap_unordered(run_test, iterable), total=len(iterable)):
        pass

    p.close()
    p.join()

    print("--- %s seconds ---" % (time.time() - start_time))
    print("----------------- TESTING FINISHES  -----------------")

if __name__ == '__main__':
    args = parser.parse_args()
    batch_size = args.batch_size
    batch_number = args.batch_number
    game_list = args.game_list
    remove_done = args.remove_done_tests

    run_tests(batch_size, batch_number, game_list, remove_done)
