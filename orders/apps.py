from django.apps import AppConfig


class OrdersConfig(AppConfig):
    name = "orders"

    def ready(self):
        from core.redis import get_redis_client
        # get_redis_client()
