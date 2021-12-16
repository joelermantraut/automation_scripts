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
Other class would give information about system, useful
to decide how many threads to use.

Really useful article to understand use of threads and processes.
https://www.toptal.com/python/beginners-guide-to-concurrency-and-parallelism-in-python#:~:text=What's%20the%20difference%20between%20Python,child%20processes%20bypassing%20the%20GIL.
"""

import threading
from queue import Queue
from time import sleep
import os


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


class ThreadSystemInfo():
    """
    Collection of functions in a class to get info about
    system cores and processes.
    """
    def __init__(self):
        pass

    def cpu_count(self):
        return os.cpu_count()


def message():
    print("Message")

def main():
    thread_control = StoppableThread(target=message)
    thread_control.start()
    sleep(2)
    thread_control.stop()

    multiple_threads = MultipleThreads(2, target=message)
    sleep(2)
    multiple_threads.stop_all()

    print(ThreadSystemInfo().cpu_count())

if __name__ == "__main__":
    main()
