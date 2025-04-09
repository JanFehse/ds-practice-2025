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


premium_user = {"Fehse", "Eulering", "Beyerle", "Einstein", "Hawking", "Newton", "Curie", "Feynman", "Bohr", "Planck"}

# Create a class to define the server functions
class OrderQueueService(order_queue_grpc.OrderQueueServiceServicer):
    # initialize the class
    def __init__(self):
        self.orders = []
        self.executors = []
    
    #Initialize into orders
    def EnqueueOrder(self, request, context):
        heapq.heappush(self.orders, (self._get_priority(request), request))
        response = order.ErrorResponse()
        response.error = False
        print("---Order Enqueued---")
        return response
    
    def DequeueOrder(self, request, context):
        if self.orders:
            _, deq_order = heapq.heappop(self.orders)
            print(f"---Order {deq_order.info.id} dequeued---")
            response = order_queue.DequeueOrderResponse(order=deq_order)
        else:
            error = order.ErrorResponse()
            error.error = True
            response = order_queue.DequeueOrderResponse(error=error)
            print("---No order or dequeueing available---")
        return response
    
    def CoordinateExecutors(self, request, context):
        idExecutor = request.portnumber
        self.executors.append(idExecutor)
        time.sleep(2)
        response = order_queue.CoordinateResponse(ids=self.executors)
        return response
    
    def _get_priority(self, order):
        is_premium = order.name in premium_user
        num_books = sum(book.quantity for book in order.booksInCart)
        # negative value for max heap
        return (-int(is_premium), -num_books, time.time())
    
    def NewElection(self, request, context):
        print("New Election called")
        exec_local = copy.deepcopy(self.executors)
        self.executors = []
        print(exec_local)
        for exec in exec_local:
            #Call all old executors in parrallel to start the election
            threading.Thread(target=self.electionAtExecutor, args=[exec]).start()
        return Empty()
    
    def electionAtExecutor(self, exec):
        try:
            with grpc.insecure_channel(exec+":50061") as channel:
                stub = executor_grpc.ExecutorServiceStub(channel)
                print("Elect Leader calling at ", exec)
                stub.ElectLeader(Empty())
        except:
            print(exec, "died")
        return
    

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    order_queue_grpc.add_OrderQueueServiceServicer_to_server(
        OrderQueueService(), server
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
