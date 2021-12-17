# -*- coding:utf-8 -*-

"""
Class that simplifies the use of multiple
threads, asynchronous, and with the ability
to have a list of which of them are alive
and to kill them.

The idea for this module is to have several classes
to control processes and threads.

One class must be to have a process stoppable.
Another one to control multiple threads automatically.

Really useful article to understand use of threads and processes.
https://www.toptal.com/python/beginners-guide-to-concurrency-and-parallelism-in-python#:~:text=What's%20the%20difference%20between%20Python,child%20processes%20bypassing%20the%20GIL.
"""

import threading
from queue import Queue
from time import sleep
import os
from functools import partial
import multiprocessing


class StoppableThread(threading.Thread):
    """
    Thread that can be controlled during execution.
    """
    def __init__(self, queue=None, *args, **kwargs):
        threading.Thread.__init__(self)
        self.queue = queue
        self.args = args
        self.kwargs = kwargs
        self._stop_event = threading.Event()

    def run(self):
        self.target = self.kwargs['target']
        try:
            self.target()
        finally:
            if self.queue:
                self.queue.task_done()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class MultipleThreads():
    """
    Class to control multiple threads with queues.

    Does a task using multiple threads, taking advantage
    of multiple cores in a processor.
    """
    def __init__(self, n_threads, *args, **kwargs):
        self.n_threads = n_threads
        # Number of threads to run
        self.queue = Queue()
        self.args = args
        self.kwargs = kwargs
        self.init()

    def init(self):
        """
        Runs all threads.
        """
        for x in range(self.n_threads):
            thread = StoppableThread(self.queue, *self.args, **self.kwargs)
            # Setting daemon to True will let the main thread exit
            # even though the workers are blocking
            thread.daemon = True
            thread.start()

            self.queue.put((thread))

    def stop_all(self):
        """
        Stops all threads.
        """
        for x in range(self.queue.qsize()):
            self.stop()

    def stop(self):
        """
        Stops one thread in each call.
        """
        thread = self.queue.get()
        thread.stop()


class MultiProcess():
    """
    Runs multiple processes in parallel.
    """
    def __init__(self, n_processes, function, *args, **kwargs):
        self.n_processes = n_processes
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.init()

    def init(self):
        self.prepare_func()

    def prepare_func(self):
        """
        Gets args from kwargs parameter.

        'freeze' must be a dict with parameters to freeze on partial
        function creation.

        'dynamic' must be a list with parameters to divide in each process.
        """
        freeze_args = dict() if 'freeze' not in self.kwargs.keys() else self.kwargs['freeze']
        dynamic_args = list() if 'dynamic' not in self.kwargs.keys() else self.kwargs['dynamic']
        partial_function = partial(self.function, **freeze_args)
        # Creates partial function with freeze args
        self._run_processes(partial_function, dynamic_args)

    def _run_processes(self, partial_function, dynamic_args):
        """
        Runs parallel processes.
        """
        with multiprocessing.Pool(self.n_processes) as p:
            p.map(partial_function, dynamic_args)
            # Calls parallel functions with dynamic args
            # This must be a list of lists... With the same number
            # of elements in childs lists as n_processes


# --------------------------------------------------
# ------------------- MAIN CODE --------------------
# --------------------------------------------------

data = [
    ['a', '2'], ['b', '4'], ['c', '6'], ['d', '8'],
    ['e', '1'], ['f', '3'], ['g', '5'], ['h', '7']
]

def mp_worker(tupla, b):
    inputs, the_time = tupla
    the_time = the_time * b
    print(f"Process {inputs}\tWaiting {the_time} seconds")
    sleep(int(the_time))
    print(f"Process {inputs}\tDONE")

def message():
    print("message")

def main():
    thread_control = StoppableThread(target=message)
    thread_control.start()
    sleep(2)
    thread_control.stop()

    multiple_threads = MultipleThreads(2, target=message)
    sleep(2)
    multiple_threads.stop_all()

    print(ThreadSystemInfo().cpu_count())

    multi = MultiProcess(2, mp_worker, dynamic=data, freeze={'b': 1})

if __name__ == "__main__":
    main()
