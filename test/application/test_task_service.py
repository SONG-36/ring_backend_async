from app.application.task_service import TaskService
from app.infrastructure.in_memory_task_repo import InMemoryTaskRepository
from app.domain.task import TaskStatus


def setup_service():
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    return service, repo


def test_submit_creates_pending_task():
    service, repo = setup_service()

    task = service.submit()

    assert task.status == TaskStatus.PENDING
    assert repo.get(task.id) is not None


def test_process_success_flow():
    service, repo = setup_service()

    task = service.submit()
    service.process(task.id)

    updated_task = repo.get(task.id)

    assert updated_task.status == TaskStatus.DONE


def test_process_retry():
    service, repo = setup_service()

    task = service.submit()

    service.process(task.id, should_fail=True)

    updated_task = repo.get(task.id)

    assert updated_task.status == TaskStatus.PENDING
    assert updated_task.retry_count == 1


def test_process_fail_to_failed():
    service, repo = setup_service()

    task = service.submit()

    service.process(task.id, should_fail=True)
    service.process(task.id, should_fail=True)

    updated_task = repo.get(task.id)

    assert updated_task.status == TaskStatus.FAILED