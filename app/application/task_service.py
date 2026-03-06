import uuid
import time
from app.domain.task import Task
from app.domain.task_repository import TaskRepository


class TaskService:

    def __init__(self, repository: TaskRepository, executor=None):
        self.repository = repository
        self.executor = executor

    def submit(self) -> Task:
        task_id = str(uuid.uuid4())
        task = Task(id=task_id)
        self.repository.save(task)

        if self.executor:
            self.executor.enqueue(task_id)

        return task

    def process(self, task_id: str) -> None:
        task = self.repository.get(task_id)
        if not task:
            raise Exception("Task not found")

        if task.status != "PENDING":
            return

        start_version = task.version

        try:
            def do_start(t):
                t.start()

            self.repository.update_with_condition(task_id, start_version, do_start)

            # Simulated work
            time.sleep(1)

            def do_complete(t):
                t.complete({"result": "ok"})

            self.repository.update_with_condition(task_id, task.version, do_complete)

        except Exception as e:

            def do_fail(t):
                t.fail(str(e))

            try:
                self.repository.update_with_condition(task_id, task.version, do_fail)
            except:
                return

            task = self.repository.get(task_id)
            if task.can_retry():
                time.sleep(2 ** task.attempt)

                def do_retry(t):
                    t.retry()

                self.repository.update_with_condition(task_id, task.version, do_retry)
                self.executor.enqueue(task_id)