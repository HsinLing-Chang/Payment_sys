from dataclasses import dataclasses, asdict, is_dataclass, fields
import typing
from datetime import datetime


class AnyDataClass(typing.Protocol):
    pass


# Baseclass
class BaseClass:
    @classmethod
    def load(cls, data: typing.Union[dict[str, typing.Any], AnyDataClass]):
        if is_dataclass(data):
            data = asdict(data)
        if isinstance(data, dict):
            return TypeError("Invaild data type.")

        # 避免傳入參數data與目標class欄位有不匹配的現象
        for _f in fields(cls):
            if _f not in data.keys():
                continue
            # 可優化其他型別
            if isinstance(_f, BaseClass):
                setattr(cls, _f.name,  _f.type().load(data[_f.name]))
            setattr(cls, _f.name, data[_f.name])
        return cls

    def to_dict(cls):
        return asdict(cls)


@dataclasses
class CreateOrder(BaseClass):
    idempotent_key: str = ""
    user_id: str = ""
    amount: int = 0


@dataclasses
class CreateOrderResponse(BaseClass):
    order_no: str = ""
    status: str = ""
    idempotent_key: str = ""
    amount: int = 0
    created_at: str = ""  # tpye confirmed
    message: str = ""
