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
# transaction_verification_pb2_grpc.TransactionVerificationServiceServicer
class TransactionVerificationService(
    transaction_verification_grpc.TransactionVerificationServiceServicer
):
    # Create an RPC function to verify transaction
    def VerifyTransaction(self, request, context):
        print("-- transaction verification called --")
        # Create a transactionResponse object
        response = transaction_verification.TransactionResponse()
        # check for valid credit card data
        if (
            len(request.CreditCard.CreditCardNumber) == 16
            and request.CreditCard.CreditCardNumber.isdigit()
            and len(request.CreditCard.cvv) == 3
            and request.CreditCard.cvv.isdigit()
            and len(request.CreditCard.expirationDate) == 5
            and request.CreditCard.expirationDate[2] == "/"
            and request.CreditCard.expirationDate[:2].isdigit()
            and request.CreditCard.expirationDate[3:].isdigit()
            and request.CreditCard.expirationDate[:2] <= "12"
            and request.CreditCard.expirationDate[1] > "0"
            and request.CreditCard.expirationDate[3:] >= "25"
        ):
            response.transactionVerified = True
            print(
                f"Verified transaction with card: {request.CreditCard.CreditCardNumber}"
            )
        else:
            response.transactionVerified = False
            print(
                f"Denied transaction with card: {request.CreditCard.CreditCardNumber}"
            )
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
    print("Transaction verification server started. Listening on port 50052.")
    # Keep thread alive
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
