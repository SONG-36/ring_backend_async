from app.domain.task_repository import TaskRepository
from app.domain.task import Task


class InMemoryTaskRepository(TaskRepository):

    def __init__(self):
        self.storage = {}

    def save(self, task: Task):
        self.storage[task.id] = task

    def get(self, task_id: str) -> Task:
        return self.storage.get(task_id)

    def update(self, task: Task):
        self.storage[task.id] = task