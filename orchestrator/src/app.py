from concurrent.futures import ThreadPoolExecutor
import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if "__file__" in globals() else os.getenv("PYTHONFILE", "")
grpc_path = os.path.abspath(
    os.path.join(FILE, "../../../utils/pb")
)
sys.path.insert(0, grpc_path)
import shared.order_pb2 as order
import shared.order_pb2_grpc as order_grpc

import fraud_detection.fraud_detection_pb2 as fraud_detection
import fraud_detection.fraud_detection_pb2_grpc as fraud_detection_grpc

import suggestions.suggestions_pb2 as suggestions
import suggestions.suggestions_pb2_grpc as suggestions_grpc

import transaction_verification.transaction_verification_pb2 as transaction_verification
import transaction_verification.transaction_verification_pb2_grpc as transaction_verification_grpc


import grpc


def detectFraud(creditCard, billingAddress):
    # Establish a connection with the fraud-detection gRPC service.
    with grpc.insecure_channel("fraud_detection:50051") as channel:
        # Create a stub object.
        print("-- Call fraud detection --")
        stub = fraud_detection_grpc.FraudDetectionServiceStub(channel)
        # Call the service through the stub object.
        request = fraud_detection.DetectFraudRequest(BillingAddress=billingAddress, CreditCard=creditCard)
        response = stub.DetectFraud(request)
    return response.isLegit

def getSuggestions(books_json):
    # Establish a connection with the fraud-detection gRPC service.
    with grpc.insecure_channel("suggestions:50053") as channel:
        # Create a stub object.
        print("-- Call suggestions --")
        stub = suggestions_grpc.SuggestionsServiceStub(channel)
        # Call the service through the stub object.
        books = []
        for book in books_json:
            books.append(suggestions.Book(bookId = 123,
                                          title = book.get("name"),
                                          author = "John Doe"))

        request = suggestions.SuggestionsRequest(booksInCart=books)
        response = stub.GetSuggestions(request)
    return response.booksSuggested

def verifyTransaction(creditCard, name, billingaddress):
    # Establish a connection with the fraud-detection gRPC service.
    with grpc.insecure_channel("transaction_verification:50052") as channel:
        # Create a stub object.
        print("-- call transaction verification --")
        stub = transaction_verification_grpc.TransactionVerificationServiceStub(channel)
        # Call the service through the stub object.
        request = transaction_verification.TransactionRequest(name = name, 
                            CreditCard = creditCard, 
                            BillingAddress=billingaddress)
        response = stub.VerifyTransaction(request)
    return response.transactionVerified


# Import Flask.
# Flask is a web framework for Python.
# It allows you to build a web application quickly.
# For more information, see https://flask.palletsprojects.com/en/latest/
from flask import Flask, request
from flask_cors import CORS
import json

# Create a simple Flask app.
app = Flask(__name__)
# Enable CORS for the app.
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/checkout", methods=["POST"])
def checkout():
    """
    Responds with a JSON object containing the order ID, status, and suggested books.
    """
    # Get request object data to json
    print("testing")
    request_data = json.loads(request.data)
    # Print request object data
    print("Request Data:", request_data.get("items"))
    Billing_Address = order.BillingAddress(
            street = request_data.get("billingAddress").get("street"), 
            city = request_data.get("billingAddress").get("city"),
            state = request_data.get("billingAddress").get("state"), 
            zip = request_data.get("billingAddress").get("zip"),
            country= request_data.get("billingAddress").get("country"))
    
    Credit_Card = order.CreditCard( CreditCardNumber = request_data.get("creditCard").get("number"), 
                            expirationDate = request_data.get("creditCard").get("expirationDate"), 
                            cvv = request_data.get("creditCard").get("cvv"), 
                        )

    with ThreadPoolExecutor(max_workers=3) as executor:
        future_isLegit = executor.submit(detectFraud, Credit_Card, Billing_Address)
        future_suggestions = executor.submit(getSuggestions,request_data.get("items"))
        future_verified = executor.submit(verifyTransaction, Credit_Card, request_data.get("name"), Billing_Address)

        isLegit = future_isLegit.result()
        suggestions = future_suggestions.result()
        verified = future_verified.result()

    print("verified: ", verified)
    print ("IsLegit: ", isLegit)
    print("suggestions:", suggestions)
    # Rest of task logic

    # Spawn new thread for each microservice
    # In each thread, call the microservie and get the response
    # Join the threads
    # Make a decision if the order is approved or not
    # Return the response

    # Dummy response following the provided YAML specification for the bookstore
    order_status_response = {
        "orderId": "12345",
        "status": "Order Approved",
        "suggestedBooks": [
            {"bookId": "123", "title": "The Best Book", "author": "Author 1"},
            {"bookId": "456", "title": "The Second Best Book", "author": "Author 2"},
        ],
    }

    return order_status_response


if __name__ == "__main__":
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host="0.0.0.0")
