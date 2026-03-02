from fastapi import FastAPI

from app.api.routes_task import router, set_task_service
from app.infrastructure.in_memory_task_repo import InMemoryTaskRepository
from app.application.task_service import TaskService
from app.application.summary_service import SummaryService
from app.infrastructure.local_executor import LocalExecutor

app = FastAPI()

repo = InMemoryTaskRepository()
summary_service = SummaryService()
task_service = TaskService(repo, summary_service)

executor = LocalExecutor(task_service)
task_service.set_executor(executor)

set_task_service(task_service)

app.include_router(router)