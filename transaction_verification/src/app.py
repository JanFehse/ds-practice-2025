import sys
import os

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

import grpc
from concurrent import futures


# Create a class to define the server functions, derived from
# transaction_verification_pb2_grpc.HelloServiceServicer
class TransactionVerificationService(
    transaction_verification_grpc.TransactionVerificationServiceServicer
):
    # Create an RPC function to verify transaction
    def VerifyTransaction(self, request, context):
        # Create a HelloResponse object
        response = transaction_verification.TransactionResponse()
        if (
            len(request.creditCard.number) == 16
            and request.creditCard.number.isdigit()
            and len(request.creditCard.cvv) == 3
            and request.creditCard.cvv.isdigit()
            and len(request.creditCard.expiryDate) == 5
            and request.creditCard.expiryDate[2] == "/"
            and request.creditCard.expiryDate[:2].isdigit()
            and request.creditCard.expiryDate[3:].isdigit()
            and request.creditCard.expiryDate[:2] <= "12"
            and request.creditCard.expiryDate[1] > "0"
            and request.creditCard.expiryDate[3:] > "25"
        ):
            response.transactionVerified = True
            print(f"Verifizierte Transaktion mit Karte: {request.creditCard.number}")
        else:
            response.transactionVerified = False
            print(
                f"Transaktion mit Karte: {request.creditCard.number} konnte nicht verifiziert werden"
            )
        # response.transactionVerified = True
        # Print the greeting message
        # print(response.transactionVerified)
        # Return the response object
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
    print("Server started. Listening on port 50052.")
    # Keep thread alive
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
