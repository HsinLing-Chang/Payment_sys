import orders.schema as schema
from tools import req_hash, get_idem_key, idem_redis_lock, update_idem_key
from tools.orders import generate_order_no
import orders.models as db
from core.common.enum import IdempKeyState, OrderStatus
from datetime import datetime, timedelta, timezone
from django.db import transaction


class OrderService:
    @staticmethod
    def createOrder(dto: schema.CreateOrder) -> schema.CreateOrderResponse:
        status = get_idem_key(dto.idempotent_key)
        hash_val = req_hash(dto.to_dict())
        print(f"idem_key status: {status}")

        if status == IdempKeyState.Done.value:
            existing_idem = db.IdempotencyKey.objects.select_related("order").filter(
                key=dto.idempotent_key,
                user_id=dto.user_id,
            ).first()
            if existing_idem and existing_idem.req_hash != hash_val:
                raise ValueError(
                    "CONFLICT: same idem_key but different request body")
            print(f"訂單已完成:{existing_idem.order.order_no}")
            return schema.CreateOrderResponse(
                order_no=existing_idem.order.order_no,
                status=existing_idem.order.status,
                idempotent_key=dto.idempotent_key,
                amount=existing_idem.order.amount,
                created_at=existing_idem.order.created_at,
                message="Idempotent response: order already created.",
            )

        lock_acquired = idem_redis_lock(dto.idempotent_key)
        if not lock_acquired:
            raise ValueError("ALREADY_EXISTS: request is processing")

        if status == IdempKeyState.Failed.value:
            # retry todo logic auto retry(?)
            existing_idem = db.IdempotencyKey.objects.select_related("order").filter(
                key=dto.idempotent_key,
                user_id=dto.user_id,
            ).first()
            if existing_idem and existing_idem.req_hash != hash_val:
                raise ValueError(
                    "CONFLICT: same idem_key but different request body")

            try:
                with transaction.atomic():
                    order = db.PaymentOrders.objects.create(
                        order_no=generate_order_no(),
                        user_id=dto.user_id,
                        amount=dto.amount,
                    )
                    existing_idem.status = IdempKeyState.Done.value
                    existing_idem.expired_at = datetime.now(
                        timezone.utc) + timedelta(days=1)
                    existing_idem.order = order
                    existing_idem.save(
                        update_fields=["status", "order_id", "expired_at"])
                update_idem_key(dto.idempotent_key, IdempKeyState.Done.value)
                print(f"已重新建立訂單:{order.order_no}")
                return schema.CreateOrderResponse(
                    order_no=order.order_no,
                    status=OrderStatus.New.value,
                    idempotent_key=dto.idempotent_key,
                    amount=dto.amount,
                    created_at=order.created_at,
                    message="Order created successfully.",
                )
            except Exception:
                update_idem_key(dto.idempotent_key,
                                IdempKeyState.Failed.value)
                raise "訂單創建失敗，稍後retry."
        else:
            try:
                with transaction.atomic():
                    order = db.PaymentOrders.objects.create(
                        order_no=generate_order_no(),
                        user_id=dto.user_id,
                        amount=dto.amount,
                    )
                    idem = db.IdempotencyKey.objects.create(
                        user_id=dto.user_id,
                        key=dto.idempotent_key,
                        order=order,
                        status=IdempKeyState.Done.value,
                        req_hash=hash_val,
                        expired_at=datetime.now(timezone.utc) +
                        timedelta(days=1),  # 過期時間設定1天
                    )
                update_idem_key(idem.key, IdempKeyState.Done.value)
                print(f"建立新訂單:{order.order_no}")
                return schema.CreateOrderResponse(
                    order_no=order.order_no,
                    status=OrderStatus.New.value,
                    idempotent_key=dto.idempotent_key,
                    amount=dto.amount,
                    created_at=order.created_at,
                    message="Order created successfully.",
                )
            except Exception:
                update_idem_key(dto.idempotent_key, IdempKeyState.Failed.value)
                raise
