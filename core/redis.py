import redis
from django.conf import settings
import logging

_pool = None


def get_redis_client():
    try:
        global _pool
        if _pool is None:
            _pool = redis.ConnectionPool(
                host=settings.REDIS["HOST"],
                port=settings.REDIS["PORT"],
                db=settings.REDIS["DB"],
                password=settings.REDIS["PASSWORD"],
                decode_responses=True,
                username=settings.REDIS["USERNAME"],
                max_connections=20,
            )
            logging.info("Redis connection successful")
        return redis.Redis(connection_pool=_pool)
    except (redis.ConnectionError, redis.TimeoutError) as e:
        logging.error("Redis connection failed: %s", e)
        raise
