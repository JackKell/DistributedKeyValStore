from queue import Queue
from threading import Thread
from threading import current_thread
from time import sleep
from time import time


def worker():
    while True:
        if (not q.empty()):
            item = q.get()
            if item is None:
                break

            print(current_thread(), item, time())
            sleep(1)
            q.task_done()


q = Queue()
threads = []
items = range(1, 11)
num_worker_threads = 3

for i in range(num_worker_threads):
    t = Thread(target=worker)
    t.start()
    threads.append(t)

for item in items:
    q.put(item)

# block until all tasks are done
q.join()

# stop workers
for i in range(num_worker_threads):
    q.put(None)
for t in threads:
    t.join()
