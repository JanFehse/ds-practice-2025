import sys
import os
import time
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
import order_queue.order_queue_pb2 as order_queue
import order_queue.order_queue_pb2_grpc as order_queue_grpc

import grpc

# Create a class to define the server functions
class OrderQueueService(order_queue_grpc.OrderQueueServiceServicer):
    orders = {}
    executors = []
    #Initialize into orders
    def EnqueueOrder(self, request, context):
        self.orders[request.info.id] = request
        response = order.ErrorResponse()
        response.error = False
        print("---Order Enqueued---")
        return response
    
    def DequeueOrder(self, request, context):
        if self.orders:
            _, deq_order = self.orders.popitem()
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
        time.sleep(1)
        response = order_queue.CoordinateResponse(ids=self.executors)
        return response


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
