from enum import Enum


class OrderStatus(Enum):
    New = "new"
    Processing = "processing"
    Failed = "failed"
    Success = "success"


class IdempKeyState(Enum):
    Done = "done"
    Failed = "failed"
