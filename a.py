import logging
import multiprocessing
import threading
import time
from games.othello.othello import Othello
from games.player import MCTS_Player
from start_async_test import generate_instances, generate_specific_instances_othello, run_test
import tqdm
from test import Test

# def thread_function(name):
#     logging.info("Thread %s: starting", name)
#     t = Test(Othello, MCTS_Player(10), MCTS_Player(10), seed = 3)
#     t.start()
#     logging.info("Thread %s: finishing", name)

import concurrent.futures

# [rest of code]

def run_tests(iterations):
    # print("thred iters: ", iterations)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(run_test, iterations)

if __name__ == "__main__":
    # format = "%(asctime)s: %(message)s"
    # logging.basicConfig(format=format, level=logging.INFO,
    #                     datefmt="%H:%M:%S")

    # with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    #     executor.map(thread_function, range(3))

    iterable = generate_instances([Othello])
    iterable += generate_specific_instances_othello()

    iterable = iterable[:10]
    print(len(iterable))

    iterable = [iterable[x:x+3] for x in range(0, len(iterable),3)]
    # print(iterable)
    # print(len(iterable))

    start_time = time.time()

    # # run_test(iterable[0])

    max_cpu = multiprocessing.cpu_count()
    p = multiprocessing.Pool(int(max_cpu))
    for _ in tqdm.tqdm(p.imap_unordered(run_tests, iterable), total=len(iterable)):
        pass
    # p.map_async(run_test, iterable)
    p.close()
    p.join()

    print("--- %s seconds ---" % (time.time() - start_time))