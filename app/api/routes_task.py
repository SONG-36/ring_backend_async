from fastapi import APIRouter
from app.utils.response import success

router = APIRouter(prefix="/tasks")

task_service = None


def set_task_service(service):
    global task_service
    task_service = service


@router.post("/report")
def create_report_task(data: dict):
    task_id = task_service.submit(
        data["sleep_hours"],
        data["steps"]
    )
    return success({"task_id": task_id})


@router.get("/{task_id}")
def get_task(task_id: str):
    task = task_service.get(task_id)

    if not task:
        return success(None, message="task not found")

    return success({
        "id": task.id,
        "status": task.status,
        "result": task.result,
        "error": task.error
    })