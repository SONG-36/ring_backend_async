import threading
import queue


class LocalExecutor:

    def __init__(self, task_service):
        self.queue = queue.Queue()
        self.task_service = task_service
        self.worker = threading.Thread(target=self.run, daemon=True)
        self.worker.start()

    def enqueue(self, task_id: str):
        self.queue.put(task_id)

    def run(self):
        while True:
            task_id = self.queue.get()
            try:
                self.task_service.process(task_id)
            except Exception as e:
                print("Worker error:", e)