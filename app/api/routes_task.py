from fastapi import APIRouter, HTTPException
from app.application.task_service import TaskService
from app.infrastructure.in_memory_task_repo import InMemoryTaskRepository
from app.infrastructure.local_executor import LocalExecutor

router = APIRouter()

# 全局单例
repo = InMemoryTaskRepository()
service = TaskService(repo)
executor = LocalExecutor(service.process)
service.executor = executor


@router.post("/tasks")
def create_task():
    task = service.submit()
    return {
        "task_id": task.id,
        "status": task.status
    }


@router.get("/tasks/{task_id}")
def get_task(task_id: str):
    task = repo.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "task_id": task.id,
        "status": task.status,
        "attempt": task.attempt,
        "result": task.result,
        "error": task.error
    }