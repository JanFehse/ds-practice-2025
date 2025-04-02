import sys
import os
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if "__file__" in globals() else os.getenv("PYTHONFILE", "")
grpc_path = os.path.abspath(os.path.join(FILE, "../../../utils/pb"))
sys.path.insert(0, grpc_path)
import shared.order_pb2 as order
import shared.order_pb2_grpc as order_grpc
import executor.executor_pb2 as executor
import executor.executor_pb2_grpc as executor_grpc

import grpc

# Create a class to define the server functions
class ExecutorService(executor_grpc.ExecutorServiceServicer):
    def dequeue(self, request, context):
        print("TODO")


def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    executor_grpc.add_ExecutorServiceServicer_to_server(
        ExecutorService(), server
    )
    # Listen on port 50051
    port = "50061"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print("Order Queue server started. Listening on port 50060.")
    # Keep thread alive
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
