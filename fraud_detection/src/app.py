import sys
import os
import random

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
grpc_path = os.path.abspath(
    os.path.join(FILE, "../../../utils/pb")
)
sys.path.insert(0, grpc_path)
import shared.order_pb2 as order
import shared.order_pb2_grpc as order_grpc
import fraud_detection.fraud_detection_pb2 as fraud_detection
import fraud_detection.fraud_detection_pb2_grpc as fraud_detection_grpc

import grpc
from concurrent import futures

# Create a class to define the server functions, derived from
# fraud_detection_pb2_grpc.FraudDetectionServiceServicer
class FraudDetectionService(fraud_detection_grpc.FraudDetectionServiceServicer):
    # Create an RPC function to detect fraud
    def DetectFraud(self, request, context):
        # Create a DetectFraudResponse object
        print("-- Detect Fraud called --")
        response = fraud_detection.DetectFraudResponse()
        # Set the greeting field of the response object
        r = random.random()
        if r < 0.05:
            response.isLegit = False
            print("-- FRAUD DETECTED --")
        else:
            response.isLegit = True
            print("-- No Fraud Detected --")
        # Return the response object
        return response

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    fraud_detection_grpc.add_FraudDetectionServiceServicer_to_server(FraudDetectionService(), server)
    # Listen on port 50051
    port = "50051"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print("Server started. Listening on port 50051.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()