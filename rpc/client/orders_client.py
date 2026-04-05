import uuid
from rpc.generated import orders_pb2, orders_pb2_grpc
import grpc
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../generated"))


def create_order(stub: orders_pb2_grpc.OrdersServiceStub, user_id: str, amount: int, idempotent_key: str = None):
    if idempotent_key is None:
        idempotent_key = uuid.uuid4().hex

    request = orders_pb2.CreateOrderRequest(
        body=orders_pb2.CreateOrderRequestBody(
            idempotent_key=idempotent_key,
            user_id=user_id,
            amount=amount,
        )
    )

    response = stub.CreateOrder(request)
    return response


def main():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = orders_pb2_grpc.OrdersServiceStub(channel)

        # 測試 1：正常建立訂單
        print("=== 測試 1：建立訂單 ===")
        idem_key = uuid.uuid4().hex
        response = create_order(stub, user_id="user_001",
                                amount=1000, idempotent_key=idem_key)
        data = response.body
        print(f"order_no      : {data.order_no}")
        print(f"status        : {data.status}")
        print(f"amount        : {data.amount}")
        print(f"idempotent_key: {data.idempotent_key}")
        print(f"message       : {data.message}")
        print(f"created_at    : {data.created_at}")

        # 測試 2：同一個 idempotent_key 重複送出（應被擋下）
        print("\n=== 測試 2：重複 idempotent_key ===")
        try:
            response2 = create_order(
                stub, user_id="user_001", amount=1000, idempotent_key=idem_key)
            data = response2.body
            print(f"order_no      : {data.order_no}")
            print(f"status        : {data.status}")
            print(f"amount        : {data.amount}")
            print(f"idempotent_key: {data.idempotent_key}")
            print(f"message       : {data.message}")
            print(f"created_at    : {data.created_at}")
        except grpc.RpcError as e:
            print(f"預期錯誤 - status: {e.code()}, detail: {e.details()}")


if __name__ == "__main__":
    main()
