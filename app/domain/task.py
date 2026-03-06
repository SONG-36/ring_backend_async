from enum import Enum
from datetime import datetime
from typing import Optional, Dict


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Task:
    def __init__(self, id: str, max_retries: int = 3):
        self.id = id
        self.status = TaskStatus.PENDING
        self.attempt = 0
        self.max_retries = max_retries
        self.result: Optional[Dict] = None
        self.error: Optional[str] = None
        self.version = 0
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def _touch(self):
        self.version += 1
        self.updated_at = datetime.utcnow()

    def start(self):
        if self.status != TaskStatus.PENDING:
            raise Exception("Task can only start from PENDING")
        self.attempt += 1
        self.status = TaskStatus.PROCESSING
        self._touch()

    def complete(self, result: Dict):
        if self.status != TaskStatus.PROCESSING:
            raise Exception("Task can only complete from PROCESSING")
        self.status = TaskStatus.COMPLETED
        self.result = result
        self.error = None
        self._touch()

    def fail(self, error: str):
        if self.status != TaskStatus.PROCESSING:
            raise Exception("Task can only fail from PROCESSING")
        self.status = TaskStatus.FAILED
        self.error = error
        self._touch()

    def can_retry(self):
        return self.status == TaskStatus.FAILED and self.attempt < self.max_retries

    def retry(self):
        if not self.can_retry():
            raise Exception("Retry not allowed")
        self.status = TaskStatus.PENDING
        self.error = None
        self._touch()