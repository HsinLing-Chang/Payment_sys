from rpc.generated import orders_pb2, orders_pb2_grpc
from orders.models import IdempotencyKey
from datetime import datetime
from orders.services import OrderService
from orders.schema import CreateOrder


class OrdersService(orders_pb2_grpc.OrdersServiceServicer):  # 實作內部細節
    def CreateOrder(self, request, context):
        try:
            order = OrderService.createOrder(
                CreateOrder().load(request.body)
            )
            return orders_pb2.CreateOrderResponse(
                order_no=order.order_no,
                status=order.status,
                idempotent_key=request.idempotent_key,
                amount=order.amount,
                created_at=order.create_at,
                message=order.message,
            )
        except ValueError as e:
            raise ("123test")
