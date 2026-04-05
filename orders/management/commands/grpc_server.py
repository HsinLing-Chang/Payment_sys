import grpc
from concurrent import futures
from django.core.management.base import BaseCommand
from rpc.generated import orders_pb2_grpc
from rpc.orders.servicer import OrdersService


class Command(BaseCommand):
    help = "Start the gRPC server"

    def add_arguments(self, parser):
        parser.add_argument(
            "--port", type=int, default=50051, help="Port to listen on (default: 50051)"
        )

    def handle(self, *args, **options):
        port = options["port"]
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=20))
        orders_pb2_grpc.add_OrdersServiceServicer_to_server(
            OrdersService(), server)
        server.add_insecure_port(f"[::]:{port}")
        server.start()
        self.stdout.write(self.style.SUCCESS(
            f"gRPC server started on port {port}"))
        server.wait_for_termination()
