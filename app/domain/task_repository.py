from abc import ABC, abstractmethod
from .task import Task


class TaskRepository(ABC):

    @abstractmethod
    def save(self, task: Task):
        pass

    @abstractmethod
    def get(self, task_id: str) -> Task:
        pass

    @abstractmethod
    def update(self, task: Task):
        pass