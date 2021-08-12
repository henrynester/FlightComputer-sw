import threading
import time
import logging
from queue import Queue


logging.basicConfig(level=logging.INFO,
                    format='(%(threadName)s) %(levelname)s: %(msg)s')


class IOThread(threading.Thread):
    def __init__(self):
        self.q = Queue()
        self.var = (1, 2, 3, 4, 5, 6, 7, 8)
        super().__init__(name='io_thread', daemon=True)

    def run(self):
        while True:
            logging.info(self.var)


t = IOThread()
logging.info('thread startup')
t.start()

t0 = time.time()
while (time.time() - t0) < 5:
    t.var = tuple([x+1 for x in t.var])


logging.info('done')
