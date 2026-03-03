import time
from app.application.task_service import TaskService
from app.infrastructure.in_memory_task_repo import InMemoryTaskRepository
from app.infrastructure.local_executor import LocalExecutor
from app.domain.task import TaskStatus


def setup_async_service():
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    executor = LocalExecutor(service.process)
    service.executor = executor
    return service, repo


def test_async_submit_should_not_block():
    service, repo = setup_async_service()

    start_time = time.time()
    task = service.submit()
    end_time = time.time()

    assert (end_time - start_time) < 0.1  # 提交应立即返回
    assert task.status == TaskStatus.PENDING


def test_async_flow_to_done():
    service, repo = setup_async_service()

    task = service.submit()

    time.sleep(0.2)  # 等待 worker 执行

    updated = repo.get(task.id)
    assert updated.status == TaskStatus.DONE


def test_multiple_tasks():
    service, repo = setup_async_service()

    tasks = [service.submit() for _ in range(10)]

    time.sleep(0.5)

    for task in tasks:
        updated = repo.get(task.id)
        assert updated.status == TaskStatus.DONE