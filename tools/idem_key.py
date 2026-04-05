import uuid
from core.redis import get_redis_client
from core.common.enum import IdempKeyState
_client = get_redis_client()  # module 載入時建立一次
_PREFIX = "idem:"
_LOCK_PREFIX = "lock_idem:"


def _key(idem_key: str, lock=False) -> str:
    if lock:
        return f"{_LOCK_PREFIX}{idem_key}"
    return f"{_PREFIX}{idem_key}"


def idem_key_generator():
    '''
    模擬clinet生成idem_key
    '''
    idem_key = uuid.uuid4().hex
    return idem_key


def idem_redis_lock(idem_key: str, ex: int = 30):
    result = _client.set(
        _key(idem_key, True), "Pending", ex=ex, nx=True)
    return result is not None


# def idem_redis_store(idem_key: str, status: str, ex: int = 86400):
#     _client.set(_key(idem_key), status, ex, nx=True)


def get_idem_key(idem_key: str):
    return _client.get(_key(idem_key))


def update_idem_key(idem_key: str, status: str, ex: int = 86400):
    _client.set(_key(idem_key), status, ex)
