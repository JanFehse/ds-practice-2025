import sys
import os
import random
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
        self.orders[request.info.id] = {"vc": [0]*self.total_svc, 'lock': threading.Lock(),
            "BillingAdress": request.BillingAddress, "Creditcard": request.CreditCard}
        response = order.ErrorResponse()
        response.error = False
        print("---detect Fraud initialized---")
        return response
    
    def update_svc(self, local_vc, incoming_vc):
        for i in range(self.total_svc):
            local_vc[i] = max(local_vc[i], incoming_vc[i])
    
    def DetectFraudBillingadress(self, request, context):
        print("-- detect Billingadress fraud start --")
        response = order.ErrorResponse()
        entry = self.orders.get(request.id)
        entry['lock'].acquire()
        self.update_svc(entry["vc"], request.vectorClock) 
        entry['lock'].release()    
        if entry["vc"] < [2,0,0]:
            response.error = False
            return response
        print("-- detect Billingadress fraud called ID:", request.id ,"--")
        r = random.random()
        if r < 0.02:
            print("-- FRAUD BILLINGADRESS DETECTED ID:", request.id ,"--")
            self.denied_order(request.id)
            response.error = False
            return response
        response.error = False
        print("-- no Fraud Detected  Billingadress ID:", request.id ,"--")
        entry['lock'].acquire()
        entry["vc"][self.svc_index] += 1
        with grpc.insecure_channel("suggestions:50053") as channel:
            stub = suggestions_grpc.SuggestionsServiceStub(channel)
            request = order.ExecInfo(id=request.id, vectorClock=entry["vc"])
            stub.GetSuggestions(request)
        entry['lock'].release()
        return response
    
    def DetectFraudCreditCard(self, request, context):
        print("-- detect CreditCard fraud start --")
        entry = self.orders.get(request.id)
        entry['lock'].acquire()
        self.update_svc(entry["vc"], request.vectorClock)
        entry['lock'].release()
        response = order.ErrorResponse()
        if entry["vc"] < [2,0,0]:
            response.error = False
            return response
        print("-- detect Creditcard fraud called ID:", request.id ,"--")
        r = random.random()
        if r < 0.02:
            print("-- FRAUD CREDITCARD DETECTED ID:", request.id ,"--")
            self.denied_order(request.id)
            response.error = False
            return response
        response.error = False
        print("-- no Fraud Detected Creditcard ID:", request.id ,"--")
        entry['lock'].acquire()
        entry["vc"][self.svc_index] += 1
        with grpc.insecure_channel("suggestions:50053") as channel:
            stub = suggestions_grpc.SuggestionsServiceStub(channel)
            request = order.ExecInfo(id=request.id, vectorClock=entry["vc"])
            stub.GetSuggestions(request)
        entry['lock'].release()
        return response
    
    def denied_order(self, id):
        orchestrator_url ='http://orchestrator:5000/callback'
        order_status_response = {
            "id": id,
            "status": "Order Rejected",
            "suggestedBooks": [],
        }
        try:
            # Sending POST request
            response = requests.post(orchestrator_url, json=order_status_response)
            # Checking response
            if response.status_code == 200:
                print("Response from orchestrator:", response.json()) 
            else:
                print("Error:", response.status_code, response.text)

        except requests.exceptions.RequestException as e:
            print("Request failed:", e)
        pass

    def DeleteOrder(self, request, context):
        print(f"--deleting id: {request.id}--")
        self.orders.pop(request.id, None)
        response = order.ErrorResponse()
        response.error = False
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
