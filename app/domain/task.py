from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    DONE = "DONE"
    FAILED = "FAILED"


@dataclass
class Task:
    id: str
    status: TaskStatus
    payload: Dict
    retry_count: int
    max_retries: int
    result: Optional[dict]
    error: Optional[str]
    created_at: datetime
    updated_at: datetime

    def start(self):
        if self.status != TaskStatus.PENDING:
            raise Exception("Invalid state transition to RUNNING")
        self.status = TaskStatus.RUNNING
        self.updated_at = datetime.utcnow()

    def complete(self, result: dict):
        if self.status != TaskStatus.RUNNING:
            raise Exception("Invalid state transition to DONE")
        self.status = TaskStatus.DONE
        self.result = result
        self.updated_at = datetime.utcnow()

    def fail(self, error: str):
        if self.status != TaskStatus.RUNNING:
            raise Exception("Invalid state transition to FAILED")

        self.retry_count += 1
        self.error = error

        if self.retry_count >= self.max_retries:
            self.status = TaskStatus.FAILED
        else:
            self.status = TaskStatus.PENDING

        self.updated_at = datetime.utcnow()