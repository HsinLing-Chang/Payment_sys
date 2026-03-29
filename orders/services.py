import orders.schema as schema
from tools.idem_key import idem_key_generator, IdempotenctStore
from tools.orders import generate_order_no
import orders.models as db
from core.common.enum import IdempKeyState, OrderStatus


class OrderService:
    def __init__(self):
        pass

    def createOrder(self, dto: schema.CreateOrder) -> schema.CreateOrderResponse:
        idem_key, user_id = dto.idempotent_key, dto.user_id
        is_existed = db.IdempotencyKey.get(key=idem_key, user_id=user_id)
        if is_existed:
            pass
            # get hash
            # get status success? => snap_hash
            #
        # 先建立訂單
        query = db.PaymentOrders(
            order_no=generate_order_no(),
            user_id=dto.user_id,
            amount=dto.amount,
        )
        query.save()

        # 建立idem_key
