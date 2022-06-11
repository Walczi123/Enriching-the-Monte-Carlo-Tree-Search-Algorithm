import argparse
from games.hex.hex import Hex
from games.hive.hive import Hive
from games.othello.othello import Othello
from start_async_test import create_tests, generate_instances, generate_specific_instances_hex, generate_specific_instances_hive, generate_specific_instances_othello, remove_done_tests, str2bool, str2game, take_batches

GAME_TYPES = [Othello, Hex, Hive]

parser = argparse.ArgumentParser(description='Script to run tests in batchs.')
parser.add_argument('-bs', "--batch_size", type=int, default=0)
parser.add_argument('-bn', "--batch_number", type=int, default=0)
parser.add_argument('-g',"--game_list", type=str2game, nargs="+", default=["Othello", "Hex", "Hive"])
parser.add_argument('-r',"--remove_done_tests", type=str2bool, nargs='?', const=True, default=True, help="Activate removing done tests.")

def count_tests(batch_size, game_list, remove_done):
    iterable = create_tests(0, 0 , game_list, remove_done)

    it_othello = [t for t in iterable if t.game_type == Othello]
    it_hex = [t for t in iterable if t.game_type == Hex]
    it_hive = [t for t in iterable if t.game_type == Hive]

    print(" ------------------------ALL--------------------------------")
    print(f"Counter of all rest tests: {len(iterable)}")
    bathces = take_batches(iterable, batch_size)
    print(f"Counter of test batches of size {batch_size}: {len(bathces)} ")
    print(" -----------------------------------------------------------")

    print(" ------------------------Othello----------------------------")
    print(f"Counter of all rest tests: {len(it_othello)}")
    bathces_othello = take_batches(it_othello, batch_size)
    print(f"Counter of test batches of size {batch_size}: {len(bathces_othello)} ")
    print(" -----------------------------------------------------------")

    print(" ------------------------Hex--------------------------------")
    print(f"Counter of all rest tests: {len(it_hex)}")
    bathces_hex = take_batches(it_hex, batch_size)
    print(f"Counter of test batches of size {batch_size}: {len(bathces_hex)} ")
    print(" -----------------------------------------------------------")

    print(" ------------------------Hive-------------------------------")
    print(f"Counter of all rest tests: {len(it_hive)}")
    bathces_hive = take_batches(it_hive, batch_size)
    print(f"Counter of test batches of size {batch_size}: {len(bathces_hive)} ")
    print(" -----------------------------------------------------------")


if __name__ == '__main__':
    args = parser.parse_args()
    batch_size = args.batch_size
    game_list = args.game_list
    remove_done = args.remove_done_tests

    count_tests(batch_size, game_list, remove_done)