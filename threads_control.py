# -*- coding:utf-8 -*-

"""
Class that simplifies the use of multiple
threads, asynchronous, and with the ability
to have a list of which of them are alive
and to kill them.
"""

import multiprocessing
import multiprocessing.dummy
import threading

class ThreadControl(object):
    """Class to control multiple threads"""
    def __init__(self):
        self.init()

    def init(self):
        pass

    def multiprocess(self, function, args, n_processes):
        """
        Creates a shared process.
        """
        with multiprocessing.Pool(n_processes) as p:
            result = p.map(function, args)

        return result

    def run_tasks(self, function, args, pool, chunk_size=None):
        """
        Run tasks receiving the pool to use.
        """
        results = pool.map(function, args, chunk_size)
        return results

    def run_process(self, function, numbers):
        """
        Runs a process pool.
        """
        p_p = multiprocessing.Pool()
        result = self.run_tasks(function, numbers, p_p)

        p_p.close()
        return result

    def run_thread(self, function, numbers):
        """
        Runs a thread pool.
        """
        t_p = multiprocessing.dummy.Pool()
        result = self.run_tasks(function, numbers, t_p)

        t_p.close()
        return result

    def async_thread(self, function, args):
        self.thread = threading.Thread(target=function, args=args)
        self.thread.start()

def power(x):
    return x**2

def main():
    thread_control = ThreadControl()
    thread_control.async_thread(power, [2])

if __name__ == "__main__":
    main()
