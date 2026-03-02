from enum import Enum
from datetime import datetime
from typing import Optional, Dict


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    DONE = "DONE"
    FAILED = "FAILED"


class Task:
    def __init__(
        self,
        id: str,
        max_retries: int = 2,
        status: TaskStatus = TaskStatus.PENDING,
        retry_count: int = 0,
        result: Optional[Dict] = None,
        error: Optional[str] = None,
    ):
        self.id = id
        self.status = status
        self.retry_count = retry_count
        self.max_retries = max_retries
        self.result = result
        self.error = error
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    # ----------------------
    # 状态机方法
    # ----------------------

    def start(self):
        if self.status != TaskStatus.PENDING:
            raise Exception("Task can only start from PENDING")
        self.status = TaskStatus.RUNNING
        self.updated_at = datetime.utcnow()

    def complete(self, result: Dict):
        if self.status != TaskStatus.RUNNING:
            raise Exception("Task can only complete from RUNNING")
        self.status = TaskStatus.DONE
        self.result = result
        self.updated_at = datetime.utcnow()

    def fail(self, error: str):
        if self.status != TaskStatus.RUNNING:
            raise Exception("Task can only fail from RUNNING")

        self.retry_count += 1
        self.error = error

        if self.retry_count < self.max_retries:
            self.status = TaskStatus.PENDING
        else:
            self.status = TaskStatus.FAILED

        self.updated_at = datetime.utcnow()