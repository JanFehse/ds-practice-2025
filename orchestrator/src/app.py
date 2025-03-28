from concurrent.futures import ThreadPoolExecutor
import threading
import random
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

import fraud_detection.fraud_detection_pb2 as fraud_detection
import fraud_detection.fraud_detection_pb2_grpc as fraud_detection_grpc

import suggestions.suggestions_pb2 as suggestions
import suggestions.suggestions_pb2_grpc as suggestions_grpc

import transaction_verification.transaction_verification_pb2 as transaction_verification
import transaction_verification.transaction_verification_pb2_grpc as transaction_verification_grpc


import grpc


def initDetectFraud(id, creditCard, billingAddress):
    # Establish a connection with the fraud-detection gRPC service.
    with grpc.insecure_channel("fraud_detection:50051") as channel:
        # Create a stub object.
        print("-- call fraud detection --")
        stub = fraud_detection_grpc.FraudDetectionServiceStub(channel)
        # Call the service through the stub object.
        execInfo = order.ExecInfo(id = id, vectorClock = [0,0,0])
        request = fraud_detection.InitDetectFraudRequest(
            info= execInfo, BillingAddress=billingAddress, CreditCard=creditCard
        )
        response = stub.InitDetectFraud(request)
    return response.error


def initSuggestions(id, books_json):
    # Establish a connection with the suggestions gRPC service.
    with grpc.insecure_channel("suggestions:50053") as channel:
        # Create a stub object.
        print("-- call suggestions --")
        stub = suggestions_grpc.SuggestionsServiceStub(channel)
        # Call the service through the stub object.
        books = []
        for book in books_json:
            books.append(
                suggestions.Book(bookId=123, title=book.get("name"), author="John Doe")
            )
        
        execInfo = order.ExecInfo(id = id, vectorClock = [0,0,0])
        request = suggestions.SuggestionsRequest(info=execInfo, booksInCart=books)
        response = stub.InitGetSuggestions(request)
    return response.error


def initVerifyTransaction(id, creditCard, name, billingaddress, books_json):
    # Establish a connection with the verify-transaction gRPC service.
    books = []
    for book in books_json:
        books.append(
            suggestions.Book(bookId=123, title=book.get("name"), author="John Doe")
        )
    with grpc.insecure_channel("transaction_verification:50052") as channel:
        # Create a stub object.
        print("-- call transaction verification --")
        stub = transaction_verification_grpc.TransactionVerificationServiceStub(channel)
        # Call the service through the stub object.
        execInfo = order.ExecInfo(id = id, vectorClock = [0,0,0])
        request = transaction_verification.TransactionRequest(
            info = execInfo, name=name, CreditCard=creditCard, BillingAddress=billingaddress, booksInCart=books
        )
        response = stub.InitVerifyTransaction(request)
    return response.error

def callVerifyTransaction(order_id):
    # Establish a connection with the verify-transaction gRPC service.
    with grpc.insecure_channel("transaction_verification:50052") as channel:
        # Create a stub object.
        print("-- start microservices --")
        stub = transaction_verification_grpc.TransactionVerificationServiceStub(channel)
        # Call the service through the stub object.
        execInfo = order.ExecInfo(id = order_id, vectorClock = [0,0,0])
        response = stub.VerifyTransaction(execInfo)
    return response.error


# Import Flask.
# Flask is a web framework for Python.
# It allows you to build a web application quickly.
# For more information, see https://flask.palletsprojects.com/en/latest/
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

# Create a simple Flask app.
app = Flask(__name__)
# Enable CORS for the app.
CORS(app, resources={r"/*": {"origins": "*"}})

response_locks = {}
responses = {}

@app.route("/checkout", methods=["POST"])
def checkout():
    """
    Responds with a JSON object containing the order ID, status, and suggested books.
    """
    # Get request object data to json
    print("-- checkout called --")
    request_data = json.loads(request.data)
    # Print request object data
    print("Request Data:", request_data.get("items"))
    Billing_Address = order.BillingAddress(
        street=request_data.get("billingAddress").get("street"),
        city=request_data.get("billingAddress").get("city"),
        state=request_data.get("billingAddress").get("state"),
        zip=request_data.get("billingAddress").get("zip"),
        country=request_data.get("billingAddress").get("country"),
    )

    Credit_Card = order.CreditCard(
        CreditCardNumber=request_data.get("creditCard").get("number"),
        expirationDate=request_data.get("creditCard").get("expirationDate"),
        cvv=request_data.get("creditCard").get("cvv"),
    )
    # Spawn new thread for each microservice
    # In each thread, call the microservie and get the response
    random_orderId = random.randint(100000, 999999)
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_initDetectFraud_error = executor.submit(initDetectFraud, random_orderId, Credit_Card, Billing_Address)
        future_initSuggestions_error = executor.submit(initSuggestions, random_orderId, request_data.get("items"))
        future_initVerifyTransaction_error = executor.submit(initVerifyTransaction, random_orderId, Credit_Card, request_data.get("name"), Billing_Address, request_data.get("items"))

        initDetectFraud_error = future_initDetectFraud_error.result()
        initSuggestions_error = future_initSuggestions_error.result()
        initVerifyTransaction_error = future_initVerifyTransaction_error.result()

    # Join the threads
    # Make a decision if the order is approved or not

    if initDetectFraud_error or initSuggestions_error or initVerifyTransaction_error: 
        return {"orderId": "123456", "status": "Order Rejected", "suggestedBooks": []}
    
    responses[random_orderId] = None
    response_locks[random_orderId] = threading.Event()

    threading.Thread(target=callVerifyTransaction, args=[random_orderId]).start() #call Function that 

    if response_locks[random_orderId].wait(timeout=5):  # Adjust timeout as needed
        response = responses.pop(random_orderId)
    else:
        print("---No response in 5 seconds for OrderID:", random_orderId)
        return {"orderId": random_orderId, "status": "Order Rejected", "suggestedBooks": []}

    suggested_books = []
    for book in response["books"]:
        suggested_books.append(
            {"bookId": book.bookId, "title": book.title, "author": book.author}
        )

    order_status_response = {
        "orderId": random_orderId,
        "status": "Order Approved" if response["status"] else "Order Rejected",
        "suggestedBooks": suggested_books,
    }
    #Return the response

    return order_status_response

@app.route('/callback', methods=['POST'])
def callback():
    """Receives responses from microservices."""
    response_data = request.json
    request_id = response_data.get("id")

    if request_id in responses:
        responses[request_id] = response_data
        response_locks[request_id].set()  # Notify waiting thread

    return jsonify({"status": "received"})


if __name__ == "__main__":
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host="0.0.0.0")
