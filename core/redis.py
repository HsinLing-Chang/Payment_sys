import redis
from django.conf import settings
import logging


def get_redis_client():
    try:
        redis_client = redis.Redis(
            host=settings.REDIS["HOST"],
            port=settings.REDIS["PORT"],
            db=settings.REDIS["DB"],
            password=settings.REDIS["PASSWORD"],
            decode_responses=True,
            username=settings.REDIS["USERNAME"],
        )
        logging.info("Redis connection successful")
        return redis_client
    except (redis.ConnectionError, redis.TimeoutError) as e:
        logging.error("Redis connection failed: %s", e)
        raise
