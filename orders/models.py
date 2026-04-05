from django.db import models
from datetime import timedelta, timezone, datetime
from core.common.enum import IdempKeyState, OrderStatus


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
    # transaction_id = models.CharField(max_length=32)
    user_id = models.CharField(max_length=32, db_index=True, null=False)
    amount = models.BigIntegerField()  # 訂單金額
    status = models.CharField(
        max_length=32, default=OrderStatus.New.value, db_index=True)

    class Meta:
        db_table = "payment_order"


class IdempotencyKey(BaseModel):
    user_id = models.CharField(max_length=32)
    key = models.CharField(max_length=128, unique=True)
    order = models.OneToOneField(
        "PaymentOrders", on_delete=models.CASCADE, related_name="idem_key", null=True, blank=True)
    status = models.CharField(
        max_length=32, default=IdempKeyState.Done.value)
    # 傳入資料的hash值，確保retry資訊一致(client req)
    req_hash = models.CharField(max_length=64)
    snap_shot = models.JSONField(
        null=True, blank=True)  # 訂單(三方)回傳結果(third_party)
    expired_at = models.DateTimeField(db_index=True)  # 過期訂單定時清理

    # index => user_id, idem_key

    class Meta:
        db_table = "idempotency_key"
        unique_together = ("user_id", "key")
# class OrderItem(BaseModel):
#     product_id = models.BigIntegerField(db_index=True)
