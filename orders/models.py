from django.db import models
from enum import Enum


class OrderStatus(Enum):
    New = "new"
    Pending = "pending"
    Processing = "processing"
    Completed = "completed"
    Failed = "failed"
    Success = "Success"


class BaseModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True


class PaymentOrders(BaseModel):
    order_no = models.CharField(  # 訂單編號
        max_length=64,
        unique=True,
        db_index=True,
    )
    amount = models.BigIntegerField()  # 訂單金額
    status = models.CharField(
        max_length=32, default=OrderStatus.New.value, db_index=True)


class IdempotencyKey(BaseModel):
    key = models.CharField(max_length=128, unique=True)
    order = models.OneToOneField(
        "PaymentOrders", on_delete=models.CASCADE, related_name="idem_key")
    status = models.CharField(
        max_length=32, default=OrderStatus.Processing.value)
    req_hash = models.CharField(max_length=64)  # 傳入資料的hash值，確保retry資訊一致
    snap_shot = models.JSONField(null=True, blank=True)  # 訂單(三方)回傳結果
