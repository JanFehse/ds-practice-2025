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
    wait_time = 5
    executors = []
    lastToken = time.time()

    def __init__(self):
        time.sleep(1)
        self.ElectLeader(Empty(), Empty())
        threading.Thread(target=self.checkToken, args=[]).start()
        return
    
    def ElectLeader(self, request, context):
        myip = socket.gethostbyname(socket.gethostname())
        with grpc.insecure_channel("order_queue:50055") as channel:
            stub = order_queue_grpc.OrderQueueServiceStub(channel)
            request = order_queue.CoordinateRequest(portnumber=myip)
            response = stub.CoordinateExecutors(request)
        self.executors = list(response.ids)
        self.myip = myip
        self.lastToken = time.time()
        if self.executors.index(myip) == 0:
            self.pass_token()
        return Empty()

    def checkToken(self):
        while time.time() - self.lastToken <= self.wait_time*(len(self.executors) + 1):
            time.sleep(self.wait_time*(len(self.executors) + 1))
        #heartbeat your predecessor
        predecessor = (self.executors.index(self.myip) + len(self.executors) - 1) % len(self.executors)
        try: 
            with grpc.insecure_channel(self.executors[predecessor]+":50061") as channel:
                stub = executor_grpc.ExecutorServiceStub(channel)
                print("Pinging ", self.executors[predecessor])
                response = stub.Ping(Empty())
        except Exception as e:
                print("error pinging", self.executors[predecessor], " Starting new leader election")
                with grpc.insecure_channel("order_queue:50055") as channel:
                    stub = order_queue_grpc.OrderQueueServiceStub(channel)
                    stub.NewElection(Empty())      
        self.lastToken = time.time()
        threading.Thread(target=self.checkToken, args=[]).start()
        return
    
    def Ping(self, request, context):
        print("Pong")
        response = order.ErrorResponse()
        response.error = False
        return response
    
    def ReceiveToken(self, request, context):
        threading.Thread(target=self.pass_token, args=[]).start()
        print("--received token--")
        self.lastToken = time.time()
        response = order.ErrorResponse(error=False)
        return response
    
    def pass_token(self):
        with grpc.insecure_channel("order_queue:50055") as channel:
            stub = order_queue_grpc.OrderQueueServiceStub(channel)
            order_response = stub.DequeueOrder(Empty())
        if not order_response.HasField("order"):
            print("No new order in queue")
            time.sleep(self.wait_time)
        else:
            threading.Thread(target=self.process_order, args=[order_response]).start()
        start = (self.executors.index(self.myip) + 1) % len(self.executors)
        had_error = True
        while had_error:
            try: 
                with grpc.insecure_channel(self.executors[start]+":50061") as channel:
                    stub = executor_grpc.ExecutorServiceStub(channel)
                    print("Passing Token to", self.executors[start])
                    pass_response = stub.ReceiveToken(Empty())
                    if not pass_response.error:
                        had_error = False
                    else:
                        raise Exception('ErrorResponse')
            except Exception as e:
                print("error passing token to", self.executors[start])        
                start = (start + 1) % len(self.executors)
        return
        
    def process_order(self, order):
        id = order.order.info.id
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
