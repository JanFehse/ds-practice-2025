import sys
import os
from concurrent.futures import ThreadPoolExecutor
import requests

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if "__file__" in globals() else os.getenv("PYTHONFILE", "")
grpc_path = os.path.abspath(os.path.join(FILE, "../../../utils/pb"))
sys.path.insert(0, grpc_path)
import shared.order_pb2 as order
import shared.order_pb2_grpc as order_grpc
import transaction_verification.transaction_verification_pb2 as transaction_verification
import transaction_verification.transaction_verification_pb2_grpc as transaction_verification_grpc
import fraud_detection.fraud_detection_pb2 as fraud_detection
import fraud_detection.fraud_detection_pb2_grpc as fraud_detection_grpc

import grpc
from concurrent import futures



class TransactionVerificationService(
    transaction_verification_grpc.TransactionVerificationServiceServicer
):
    orders = {}
    
    # Queue the transaction for verification
    def InitVerifyTransaction(self, request, context):
        self.orders[request.info.id] = {"data": request}
        print("-- transaction verification called - transaction queued --")
        response = order.ErrorResponse()
        response.error = False
        return response
    
    def VerifyTransaction(self, request, context):
        id = request.id
        print(f"-- transaction verification called for order {id} --")
        response = order.ErrorResponse()
        
        verifiedCart = self.VerifyCart(id)
        
        if not verifiedCart:
            self.denied_order(id)
            response.error = False
            return response
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_verifyUserData = executor.submit(self.VerifyUserData, id)
            future_verifyCreditCardData = executor.submit(self.VerifyCreditCardData, id)
            results = {
                "userDataVerified": future_verifyUserData.result(),
                "creditCardVerified": future_verifyCreditCardData.result()
            }
        response.error = False
        return response
            
    # check for non empty cart
    def VerifyCart(self, id):
        print(f"-- transaction verification - verify cart for order {id} --")

        if id not in self.orders or "data" not in self.orders[id]:
            print(f"Order {id} not found")
            return False

        order_data = self.orders[id]["data"]
        if hasattr(order_data, "booksInCart") and len(order_data.booksInCart) > 0:
            print(f"Verified cart with {len(order_data.booksInCart)} books")
            order_data.info.vectorClock[0] += 1
            return True
        else:
            print("Denied cart with no books")
            return False
    
    
    def VerifyUserData(self, id):
        print(f"-- transaction verification - verify user data for order {id} --")
        order_data = self.orders[id]["data"]
        if (
            hasattr(order_data, "name")
            and hasattr(order_data, "BillingAddress")
            and hasattr(order_data.BillingAddress, "street")
            and hasattr(order_data.BillingAddress, "city")
            and hasattr(order_data.BillingAddress, "state")
            and hasattr(order_data.BillingAddress, "zip")
            and hasattr(order_data.BillingAddress, "country")
        ):
            print(f"Verified user data for order {id}")
            order_data.info.vectorClock[0] += 1
            with grpc.insecure_channel("fraud_detection:50051") as channel:
                stub = fraud_detection_grpc.FraudDetectionServiceStub(channel)
                request = order.ExecInfo(id = id, vectorClock = order_data.info.vectorClock)
                stub.DetectFraudBillingadress(request)
            return True
        else:    
            print(f"Denied user data for order {id}")
            self.denied_order(id)
            return False
    
    def VerifyCreditCardData(self, id):
        print(f"-- transaction verification - verify credit card data for order {id} --")
        order_data = self.orders[id]["data"]
        if (
            len(order_data.CreditCard.CreditCardNumber) == 16
            and order_data.CreditCard.CreditCardNumber.isdigit()
            and len(order_data.CreditCard.cvv) == 3
            and order_data.CreditCard.cvv.isdigit()
            and len(order_data.CreditCard.expirationDate) == 5
            and order_data.CreditCard.expirationDate[2] == "/"
            and order_data.CreditCard.expirationDate[:2].isdigit()
            and order_data.CreditCard.expirationDate[3:].isdigit()
            and order_data.CreditCard.expirationDate[:2] <= "12"
            and order_data.CreditCard.expirationDate[1] > "0"
            and order_data.CreditCard.expirationDate[3:] >= "25"
        ):
            print(
                f"Verified credit card for order {id}"
            )
            order_data.info.vectorClock[0] += 1
            with grpc.insecure_channel("fraud_detection:50051") as channel:
                stub = fraud_detection_grpc.FraudDetectionServiceStub(channel)
                request = order.ExecInfo(id = id, vectorClock = order_data.info.vectorClock)
                stub.DetectFraudCreditCard(request)
            return True
        else:
            print(
                f"Denied credit card for order {id}"
            )
            self.denied_order(id)
            return False
    
    def denied_order(id):
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
        
    def DeleteOrder(self, request, context):
        self.orders.pop(request.id, None)
        response = order.ErrorResponse()
        response.error = False
        return response


def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    transaction_verification_grpc.add_TransactionVerificationServiceServicer_to_server(
        TransactionVerificationService(), server
    )
    # Listen on port 50052
    port = "50052"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print("Transaction verification server started. Listening on port 50052.")
    # Keep thread alive
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
