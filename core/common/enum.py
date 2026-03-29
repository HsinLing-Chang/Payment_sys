from enum import Enum


class OrderStatus(Enum):
    New = "new"
    Processing = "processing"
    Failed = "failed"
    Success = "success"


class IdempKeyState(Enum):
    Pending = "pending"
    Done = "done"
    Failed = "failed"
