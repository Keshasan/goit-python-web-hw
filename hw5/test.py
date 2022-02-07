from multiprocessing import Process
import os
from concurrent.futures import ProcessPoolExecutor
import time


def find_dividers(number):
    print(f'pid = {os.getpid()}')
    result = []
    for counter in range(1, number+1):
        if number % counter == 0:
            result.append(counter)
    return result


def proc_factorize(*numbers):

    with ProcessPoolExecutor(max_workers=4) as executor:
        return executor.map(find_dividers, numbers)


if __name__ == '__main__':
    start = time.time()
    a, b, c, d = proc_factorize(128, 255, 99999, 10651060)
    print('PoolMultiProc version done in {:.4f} seconds'.format(
        time.time()-start))
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
                 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
