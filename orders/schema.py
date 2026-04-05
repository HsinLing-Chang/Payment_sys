from dataclasses import dataclass, asdict, is_dataclass, fields
import typing
from datetime import datetime
from google.protobuf.message import Message
from google.protobuf.json_format import MessageToDict


class AnyDataClass(typing.Protocol):
    pass


@dataclass
class BaseClass:
    def load(self, data: typing.Union[dict[str, typing.Any], AnyDataClass, Message]):
        if is_dataclass(data):
            data = asdict(data)
        elif isinstance(data, Message):
            data = MessageToDict(data, preserving_proto_field_name=True)
        if not isinstance(data, dict):
            raise TypeError("Invaild data type.")

        # 避免傳入參數data與目標class欄位有不匹配的現象
        for _f in fields(self):
            if _f.name not in data.keys():
                continue
            # 可優化其他型別
            if issubclass(_f.type, BaseClass):
                setattr(self, _f.name,  _f.type().load(data[_f.name]))
            setattr(self, _f.name, _f.type(data[_f.name]))
        return self

    def to_dict(self):
        return asdict(self)


@dataclass
class CreateOrder(BaseClass):
    idempotent_key: str = ""
    user_id: str = ""
    amount: int = 0


@dataclass
class CreateOrderResponse(BaseClass):
    order_no: str = ""
    status: str = ""
    idempotent_key: str = ""
    amount: int = 0
    created_at: str = ""  # tpye confirmed
    message: str = ""
