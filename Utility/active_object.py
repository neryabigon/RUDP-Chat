#  basic active object class
from threading import Thread, Condition
from queue import Queue


class ActiveObject:
    def __init__(self):
        self._handlers = []
        self._queue = Queue()
        self._cond = Condition()
        self.thread = Thread(target=self.run, daemon=True)
        self.thread.start()

    def add_handler(self, handler):
        self._handlers.append(handler)

    def remove_handler(self, handler):
        self._handlers.remove(handler)

    def run(self):
        while self._queue.empty():
            self._cond.wait()
            try:
                event = self._queue.get()
            except Exception as e:
                print(e)
                continue
            for handler in self._handlers:
                handler(event)
