from abc import ABC, abstractmethod
from typing import Optional
from app.domain.task import Task


class TaskRepository(ABC):

    @abstractmethod
    def save(self, task: Task) -> None:
        pass

    @abstractmethod
    def get(self, task_id: str) -> Optional[Task]:
        pass

    @abstractmethod
    def update(self, task: Task) -> None:
        pass