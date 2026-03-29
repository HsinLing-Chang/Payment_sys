**Proto生成指令**:
在 payment/ 根目錄執行

```
python -m grpc_tools.protoc \
    -I rpc/protos \
    --python_out=rpc/generated \
    --grpc_python_out=rpc/generated \
    rpc/protos/orders.proto
-I rpc/protos：告訴 protoc 去哪找 .proto 檔
--python_out：產生 orders_pb2.py（message 類別）
--grpc_python_out：產生 orders_pb2_grpc.py（servicer/stub 類別）
```

**_idem_key表可存入因網路問題產生的斷點<recovery_point>_**
