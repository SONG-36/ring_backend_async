import uuid
from app.domain.task import Task
from app.domain.task_repository import TaskRepository


class TaskService:

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def submit(self) -> Task:
        task_id = str(uuid.uuid4())
        task = Task(id=task_id)
        self.repository.save(task)
        return task

    def process(self, task_id: str, should_fail: bool = False) -> None:
        task = self.repository.get(task_id)

        if not task:
            raise Exception("Task not found")

        task.start()
        self.repository.update(task)

        try:
            if should_fail:
                raise Exception("Simulated failure")

            task.complete({"result": "ok"})

        except Exception as e:
            task.fail(str(e))

        self.repository.update(task)