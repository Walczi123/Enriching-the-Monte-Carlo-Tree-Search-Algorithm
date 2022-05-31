import multiprocessing
import time
import tqdm
import argparse
from games.hex.hex import Hex
from start_async_test import generate_instances, generate_specific_instances_hex, run_test, take_batch

parser = argparse.ArgumentParser(description='Script to run tests in batchs.')
parser.add_argument("--batch_size", type=int, default=0)
parser.add_argument("--batch_number", type=int, default=0)

def run_tests(batch_size, batch_number):
    iterable = generate_instances([Hex])
    iterable += generate_specific_instances_hex()

    print(f"batch size: {batch_size}, batch number: {batch_number}")
    iterable = take_batch(iterable, batch_size, batch_number)
    if iterable == None:
        print("nothing to test")
        return

    start_time = time.time()
    max_cpu = multiprocessing.cpu_count()
    p = multiprocessing.Pool(int(max_cpu))
    for _ in tqdm.tqdm(p.imap_unordered(run_test, iterable), total=len(iterable)):
        pass
    p.close()
    p.join()

    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    args = parser.parse_args()

    batch_size = args.batch_size
    batch_number = args.batch_number
    run_tests(batch_size, batch_number)
