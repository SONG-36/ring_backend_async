from typing import Dict, Optional
import threading
from app.domain.task import Task
from app.domain.task_repository import TaskRepository


class InMemoryTaskRepository(TaskRepository):

    def __init__(self):
        self.storage: Dict[str, Task] = {}
        self.lock = threading.Lock()

    def save(self, task: Task) -> None:
        with self.lock:
            self.storage[task.id] = task

    def get(self, task_id: str) -> Optional[Task]:
        with self.lock:
            return self.storage.get(task_id)

    def update_with_condition(self, task_id: str, expected_version: int, update_fn):
        with self.lock:
            task = self.storage.get(task_id)
            if not task:
                raise Exception("Task not found")
            if task.version != expected_version:
                raise Exception("Concurrency conflict")
            update_fn(task)
            self.storage[task_id] = task
            return task