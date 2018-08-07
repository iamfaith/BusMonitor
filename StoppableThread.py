import threading

import time


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, custom_func=None, args=()):
        super(StoppableThread, self).__init__()
        self._stop_event = threading.Event()
        self.func = custom_func
        self.args = args

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        while True:
            if self.stopped():
                break
            try:
                if self.func:
                    if self.func(self.args):
                        break
            finally:
                pass


def loop(text):
    print('hello' + text)
    time.sleep(3)
    return True


if __name__ == '__main__':
    t = StoppableThread(loop, 'asd')
    t.start()
    time.sleep(7)
    t.stop()
