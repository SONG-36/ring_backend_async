import time
from app.application.task_service import TaskService
from app.infrastructure.in_memory_task_repo import InMemoryTaskRepository
from app.infrastructure.local_executor import LocalExecutor
from app.domain.task import TaskStatus


def setup_service():
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    executor = LocalExecutor(service.process)
    service.executor = executor
    return service, repo


def test_process_success_flow():
    repo = InMemoryTaskRepository()
    service = TaskService(repo, failure_strategy=lambda t: False)

    task = service.submit()
    service.process(task.id)

    updated = repo.get(task.id)
    assert updated.status == TaskStatus.DONE


def test_process_retry():
    repo = InMemoryTaskRepository()

    call_count = {"count": 0}

    def fail_once(task):
        call_count["count"] += 1
        return call_count["count"] == 1

    service = TaskService(repo, failure_strategy=fail_once)

    task = service.submit()
    service.process(task.id)
    service.process(task.id)

    updated = repo.get(task.id)

    assert updated.retry_count == 1
    assert updated.status == TaskStatus.DONE