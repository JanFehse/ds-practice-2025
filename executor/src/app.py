import sys
import os
import time
import socket
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
import executor.executor_pb2 as executor
import executor.executor_pb2_grpc as executor_grpc
import order_queue.order_queue_pb2 as order_queue
import order_queue.order_queue_pb2_grpc as order_queue_grpc

import grpc

# Create a class to define the server functions
class ExecutorService(executor_grpc.ExecutorServiceServicer):
    executors = []
    def __init__(self):
        myip = socket.gethostbyname(socket.gethostname())
        time.sleep(1)
        with grpc.insecure_channel("order_queue:50055") as channel:
            stub = order_queue_grpc.OrderQueueServiceStub(channel)
            request = order_queue.CoordinateRequest(portnumber=myip)
            response = stub.CoordinateExecutors(request)
        self.executors = list(response.ids)
        self.myip = myip
        if self.executors.index(myip) == 0:
            self.pass_token()
        return
    
    def ReceiveToken(self, request, context):
        threading.Thread(target=self.pass_token, args=[]).start()
        print("--received token--")
        response = order.ExecInfo(error=False)
        return response
    
    def pass_token(self):
        with grpc.insecure_channel("order_queue:50055") as channel:
            stub = order_queue_grpc.OrderQueueServiceStub(channel)
            order_response = stub.DequeueOrder(Empty())
        print(order_response)
        if order_response.info.error:
            print("No new order in queue")
            time.sleep(2)
        else:
            threading.Thread(target=self.process_order, args=[order_response]).start()
        start = (self.executors.index(self.myip) + 1) % len(self.executors)
        had_error = True
        while had_error:
            try: 
                with grpc.insecure_channel(self.executors[start]+"50061") as channel:
                    stub = executor_grpc.ExecutorServiceStub(channel)
                    print("Passing Token to", self.executors[start])
                    pass_response = stub.ReceiveToken(Empty())
                    if not pass_response.error:
                        had_error = False
                    else:
                        raise Exception('ErrorResponse')
            except:
                print("error passing token to", self.executors[start])        
                start = (start + 1) % len(self.executors)
        return
        
    def process_order(self, order):
        id = order.info.id
        print("processing order with id: ", id)
        return

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
