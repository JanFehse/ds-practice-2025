import sys
import os
import random

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if "__file__" in globals() else os.getenv("PYTHONFILE", "")
grpc_path = os.path.abspath(os.path.join(FILE, "../../../utils/pb"))
sys.path.insert(0, grpc_path)
import shared.order_pb2 as order
import shared.order_pb2_grpc as order_grpc
import fraud_detection.fraud_detection_pb2 as fraud_detection
import fraud_detection.fraud_detection_pb2_grpc as fraud_detection_grpc
import suggestions.suggestions_pb2 as suggestions
import suggestions.suggestions_pb2_grpc as suggestions_grpc

import grpc
from concurrent import futures


# Create a class to define the server functions, derived from
# fraud_detection_pb2_grpc.FraudDetectionServiceServicer
class FraudDetectionService(fraud_detection_grpc.FraudDetectionServiceServicer):
    orders = {}
    total_svc = 3
    svc_index = 1
    #Initialize into orders
    def InitDetectFraud(self, request, context):
        print("---detect Fraud initialized---")
        self.orders[request.info.id] = {"vc": [0]*self.total_svc, "BillingAdress": request.BillingAddress, "Creditcard": request.CreditCard}
        response = order.ErrorResponse()
        response.error = False
        return response
    
    def update_svc(self, local_vc, incoming_vc):
        for i in range(self.total_svc):
            local_vc[i] = max(local_vc[i], incoming_vc[i])
    
    def DetectFraudBillingadress(self, request, context):
        entry = self.orders.get(request.id)
        self.update_svc(entry["vc"], request.vectorClock)
        response = order.ErrorResponse()
        if entry["vc"] < [2,0,0]:
            response.error = False
            return response
        print("-- detect Billingadress fraud called ID:", request.id ,"--")
        r = random.random()
        if r < 0.02:
            print("-- FRAUD BILLINGADRESS DETECTED ID:", request.id ,"--")
            # TODO call Orchestrator that the order should not be finished
        response.error = False
        print("-- no Fraud Detected ID:", request.id ,"--")
        entry["vc"][self.svc_index] += 1
        with grpc.insecure_channel("suggestions:50053") as channel:
            stub = suggestions_grpc.SuggestionsServiceStub(channel)
            request = order.ExecInfo(id=request.id, vectorClock=entry["vc"])
            stub.GetSuggestions(request)
        return response
    
    def DetectFraudCreditCard(self, request, context):
        entry = self.orders.get(request.id)
        self.update_svc(entry["vc"], request.vectorClock)
        response = order.ErrorResponse()
        if entry["vc"] < [2,0,0]:
            response.error = False
            return response
        print("-- detect Creditcard fraud called ID:", request.id ,"--")
        r = random.random()
        if r < 0.02:
            print("-- FRAUD CREDITCARD DETECTED ID:", request.id ,"--")
            # TODO call Orchestrator that the order should not be finished
        response.error = False
        print("-- no Fraud Detected Creditcard ID:", request.id ,"--")
        entry["vc"][self.svc_index] += 1
        with grpc.insecure_channel("suggestions:50053") as channel:
            stub = suggestions_grpc.SuggestionsServiceStub(channel)
            request = order.ExecInfo(id=request.id, vectorClock=entry["vc"])
            stub.GetSuggestions(request)
        return response


def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    fraud_detection_grpc.add_FraudDetectionServiceServicer_to_server(
        FraudDetectionService(), server
    )
    # Listen on port 50051
    port = "50051"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print("Fraud detection server started. Listening on port 50051.")
    # Keep thread alive
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
