from datetime import datetime, timezone, timedelta
from core.redis import get_redis_client


def generate_order_no():
    datatime_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    redis_key = f"order_no:{datatime_str}"
    r = get_redis_client()
    seq = 100000 + r.incr(redis_key)
    if seq == 100001:
        r.expire(redis_key, 86400*2)

    return f"ORD{datatime_str}{seq}"
