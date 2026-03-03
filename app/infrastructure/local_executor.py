import threading
import queue
from typing import Callable


class LocalExecutor:
    def __init__(self, handler: Callable[[str], None]):
        self.queue = queue.Queue()
        self.handler = handler
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()

    def enqueue(self, task_id: str):
        self.queue.put(task_id)

    def _worker_loop(self):
        while True:
            task_id = self.queue.get()
            try:
                self.handler(task_id)
            except Exception as e:
                print(f"Worker error: {e}")
            finally:
                self.queue.task_done()