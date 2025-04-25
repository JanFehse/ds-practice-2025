import random
import sys
import os
import requests
import threading
# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if "__file__" in globals() else os.getenv("PYTHONFILE", "")
grpc_path = os.path.abspath(os.path.join(FILE, "../../../utils/pb"))
sys.path.insert(0, grpc_path)
import shared.order_pb2 as order
import shared.order_pb2_grpc as order_grpc
import payment.payment_pb2 as payment
import payment.payment_pb2_grpc as payment_grpc


import grpc
from concurrent import futures


# Create a class to define the server functions, derived from
# fraud_detection_pb2_grpc.HelloServiceServicer
class PaymentService(payment_grpc.PaymentsServiceServicer):
    prepared = False

    def __init__(self):
        self.prepared = False
        return

    def Prepare(self,request,context):
        #Todo dummy logic
        self.prepared = True
        response = order.ErrorResponse()
        response.error = False
        return response
    
    def Commit(self,request,context):
        response = order.ErrorResponse()
        if(self.prepared):
            self.prepared = False
            print(f"Payment commited for OrderId: {request.id}")
            response.error = False
            return response
        response.error = True
        return response
    
    def Abort(self,request,context):
        self.prepared = False
        print(f"Payment aborted for OrderId: {request.id}")
        response = order.ErrorResponse()
        response.error = True
        return response


def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add PaymentService
    payment_grpc.add_PaymentsServiceServicer_to_server(
        PaymentService(), server
    )
    # Listen on port 50051
    port = "50053"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print("Payment server started. Listening on port 50053.")
    # Keep thread alive
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
