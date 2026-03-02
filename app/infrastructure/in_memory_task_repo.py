from typing import Dict, Optional
from app.domain.task import Task
from app.domain.task_repository import TaskRepository


class InMemoryTaskRepository(TaskRepository):

    def __init__(self):
        self.storage: Dict[str, Task] = {}

    def save(self, task: Task) -> None:
        self.storage[task.id] = task

    def get(self, task_id: str) -> Optional[Task]:
        return self.storage.get(task_id)

    def update(self, task: Task) -> None:
        self.storage[task.id] = task