import multiprocessing
import random
import time
from games.hive.hive import Hive
from start_async_test import generate_instances, generate_specific_instances_hive, run_test
import tqdm
import numpy as np


def run_tests():
    iterable = generate_instances([Hive])
    iterable += generate_specific_instances_hive()

    # for i in iterable:
    #     run_test(i)

    random.shuffle(iterable)

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
    run_tests()
