import uuid
from datetime import datetime

from app.domain.task import Task, TaskStatus


class TaskService:

    def __init__(self, repo, summary_service):
        self.repo = repo
        self.summary_service = summary_service
        self.executor = None

    def set_executor(self, executor):
        self.executor = executor

    def submit(self, sleep_hours: float, steps: int) -> str:
        task_id = str(uuid.uuid4())
        now = datetime.utcnow()

        payload = {
            "sleep_hours": sleep_hours,
            "steps": steps
        }

        task = Task(
            id=task_id,
            status=TaskStatus.PENDING,
            payload=payload,
            retry_count=0,
            max_retries=3,
            result=None,
            error=None,
            created_at=now,
            updated_at=now
        )

        self.repo.save(task)
        self.executor.enqueue(task_id)

        return task_id

    def process(self, task_id: str):
        task = self.repo.get(task_id)

        if not task:
            return

        if task.status in (TaskStatus.DONE, TaskStatus.FAILED):
            return

        task.start()
        self.repo.update(task)

        try:
            result = self.summary_service.generate(
                task.payload["sleep_hours"],
                task.payload["steps"]
            )
            task.complete(result)
        except Exception as e:
            task.fail(str(e))

        self.repo.update(task)

    def get(self, task_id: str):
        return self.repo.get(task_id)