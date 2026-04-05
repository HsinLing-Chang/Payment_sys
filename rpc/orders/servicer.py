from rpc.generated import orders_pb2, orders_pb2_grpc
from orders.models import IdempotencyKey
from datetime import datetime
from orders.services import OrderService
from orders.schema import CreateOrder
import grpc


class OrdersService(orders_pb2_grpc.OrdersServiceServicer):  # 實作內部細節
    def CreateOrder(self, request, context):
        try:
            print(request.body)
            order = OrderService.createOrder(
                CreateOrder().load(request.body)
            )
            return orders_pb2.CreateOrderResponse(
                body=orders_pb2.CreateOrderResponseBody(
                    order_no=order.order_no,
                    status=order.status,
                    idempotent_key=order.idempotent_key,
                    amount=order.amount,
                    created_at=order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    message=order.message,
                )
            )
        except ValueError as e:
            context.abort(grpc.StatusCode.ALREADY_EXISTS, str(e))
