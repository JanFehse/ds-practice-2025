import sys
import os
import time
import grpc
import heapq
import copy
import threading
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
from google.protobuf.empty_pb2 import Empty

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if "__file__" in globals() else os.getenv("PYTHONFILE", "")
grpc_path = os.path.abspath(os.path.join(FILE, "../../../utils/pb"))
sys.path.insert(0, grpc_path)
import shared.order_pb2 as order
import shared.order_pb2_grpc as order_grpc
import order_queue.order_queue_pb2 as order_queue
import order_queue.order_queue_pb2_grpc as order_queue_grpc
import executor.executor_pb2 as executor
import executor.executor_pb2_grpc as executor_grpc


# Create a class to define the server functions
class DatabaseService(order_queue_grpc.DatabaseServiceServicer):
    # initialize the class
    def __init__(self):
        self.orders = {}
        return 
    

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    order_queue_grpc.add_DatabaseServiceServicer_to_server(
        DatabaseService(), server
    )
    # Listen on port 50051
    port = "50055"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print("Order Queue server started. Listening on port 50055.")
    # Keep thread alive
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
