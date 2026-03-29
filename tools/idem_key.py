import uuid
from core.redis import get_redis_client


class IdempotenctStore:
    def __init__(self):
        self.client = get_redis_client()
        self.prefix = "idem:"

    def _key(self, idem_key: str) -> str:
        return f"{self.prefix}{idem_key}"

    def idem_key_generator(self):
        '''
        模擬clinet生成idem_key
        '''
        idem_key = uuid.uuid4().hex
        return idem_key
