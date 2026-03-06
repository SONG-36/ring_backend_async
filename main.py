from app.infrastructure.in_memory_task_repo import InMemoryTaskRepository
from app.infrastructure.local_executor import LocalExecutor
from app.application.task_service import TaskService

repo = InMemoryTaskRepository()
service = TaskService(repo)
executor = LocalExecutor(service.process)
service.executor = executor

# Submit multiple tasks
for _ in range(5):
    service.submit()

# Keep process alive
import time
while True:
    time.sleep(5)