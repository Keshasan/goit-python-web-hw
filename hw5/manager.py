from multiprocessing import Process, Manager
import os
import time


def find_dividers(number, l):
    print(f'pid = {os.getpid()}')
    result = []
    for counter in range(1, number+1):
        if number % counter == 0:
            l.append(counter)


def factorize(*numbers):
    result = []
    st = time.time()
    with Manager() as manager:
        for number in numbers:
            l = manager.list([])

            p = Process(target=find_dividers, args=(number, l), daemon=False)
            p.start()
            p.join()
            result.append(l[:])
    print('ManagerMultiProc version done in {:.4f} seconds'.format(
        time.time()-st))
    return result


if __name__ == '__main__':

    a, b, c, d = factorize(128, 255, 99999, 10651060)

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316,
                 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
