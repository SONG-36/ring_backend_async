import pytest
from app.domain.task import Task, TaskStatus


def new_task():
    return Task(id="1", max_retries=2)


def test_pending_to_running():
    task = new_task()
    task.start()
    assert task.status == TaskStatus.RUNNING

def test_full_success_flow():
    task = new_task()
    task.start()
    task.complete({"ok": True})
    assert task.status == TaskStatus.DONE

def test_illegal_double_start():
    task = new_task()
    task.start()
    with pytest.raises(Exception):
        task.start()

def test_retry_back_to_pending():
    task = new_task()
    task.start()
    task.fail("error")
    assert task.status == TaskStatus.PENDING
    assert task.retry_count == 1

def test_retry_to_failed():
    task = new_task()
    task.start()
    task.fail("error")
    task.start()
    task.fail("error")
    assert task.status == TaskStatus.FAILED

def test_done_cannot_restart():
    task = new_task()
    task.start()
    task.complete({"ok": True})
    with pytest.raises(Exception):
        task.start()