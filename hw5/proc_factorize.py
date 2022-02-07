from multiprocessing import Process
import os

import time
from multiprocessing import Pool


def find_dividers(number):
    print(f'pid = {os.getpid()}')
    result = []
    for counter in range(1, number+1):
        if number % counter == 0:
            result.append(counter)
    return result


def factorize(*numbers) -> list:

    result = []
    for number in numbers:
        counters = find_dividers(number)
        result.append(counters)

    return result


def proc_factorize(*numbers):
    with Pool(processes=len(numbers)) as pool:
        return pool.map(find_dividers, numbers)


if __name__ == '__main__':
    # Sync Version
    start_time = time.time()
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    print('Sync version done in {:.4f} seconds'.format(
        time.time()-start_time))

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
                 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

    # MultiProc Version
    start_time = time.time()
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    print('PoolMultiProc version done in {:.4f} seconds'.format(
        time.time()-start_time))

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
                 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    # nums = [128, 255, 99999, 10651060]
    # with Pool(processes=len(nums)) as pool:
    #     print(pool.map(find_dividers, nums))
    # print('MultipProc version done in {:.4f} seconds'.format(
    #     time.time()-start_time))
