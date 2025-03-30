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

import order_queue.order_queue_pb2 as order_queue
import order_queue.order_queue_pb2_grpc as order_queue_grpc

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

def deleteOrderIdSuggestions(order_id):
    with grpc.insecure_channel("suggestions:50053") as channel:
        stub = suggestions_grpc.SuggestionsServiceStub(channel)
        execInfo = order.ExecInfo(id = order_id, vectorClock = [0,0,0])
        response = stub.DeleteOrder(execInfo)
    return response.error

def deleteOrderIdTransaction(order_id):
    with grpc.insecure_channel("transaction_verification:50052") as channel:
        stub = transaction_verification_grpc.TransactionVerificationServiceStub(channel)
        execInfo = order.ExecInfo(id = order_id, vectorClock = [0,0,0])
        response = stub.DeleteOrder(execInfo)
    return response.error

def deleteOrderIdFraudDetection(order_id):
    with grpc.insecure_channel("fraud_detection:50051") as channel:
        stub = fraud_detection_grpc.FraudDetectionServiceStub(channel)
        execInfo = order.ExecInfo(id = order_id, vectorClock = [0,0,0])
        response = stub.DeleteOrder(execInfo)
    return response.error

def deleteId(order_id):
    print("--delete rejected id--")
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_deleteOrderIdDetectFraud_error = executor.submit(deleteOrderIdFraudDetection, order_id)
        future_deleteOrderIdSuggestions_error = executor.submit(deleteOrderIdTransaction, order_id)
        future_deleteOrderIdVerifyTransaction_error = executor.submit(deleteOrderIdSuggestions, order_id)

        deleteOrderIdDetectFraud_error = future_deleteOrderIdDetectFraud_error.result()
        deleteOrderIdSuggestions_error = future_deleteOrderIdSuggestions_error.result()
        deleteOrderIdVerifyTransaction_error = future_deleteOrderIdVerifyTransaction_error.result()
    
    if deleteOrderIdDetectFraud_error or deleteOrderIdSuggestions_error or deleteOrderIdVerifyTransaction_error:
        print("--Error deleting Id--")
    pass 
    

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
global_id = 100000
id_lock = threading.Lock()

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
    
    Ordered_Books = []
    for item in request_data.get("items"):
        Ordered_Books.append(order_queue.OrderedBook(
            title=item.get("name"),
            quantity=item.get("quantity")
        ))
    
    # Spawn new thread for each microservice
    # In each thread, call the microservie and get the response
    global global_id
    global id_lock
    id_lock.acquire()
    order_id = global_id
    global_id += 1
    id_lock.release()
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_initDetectFraud_error = executor.submit(initDetectFraud, order_id, Credit_Card, Billing_Address)
        future_initSuggestions_error = executor.submit(initSuggestions, order_id, request_data.get("items"))
        future_initVerifyTransaction_error = executor.submit(initVerifyTransaction, order_id, Credit_Card, request_data.get("name"), Billing_Address, request_data.get("items"))

        initDetectFraud_error = future_initDetectFraud_error.result()
        initSuggestions_error = future_initSuggestions_error.result()
        initVerifyTransaction_error = future_initVerifyTransaction_error.result()

    # Join the threads
    # Make a decision if the order is approved or not

    if initDetectFraud_error or initSuggestions_error or initVerifyTransaction_error: 
        return {"orderId": "123456", "status": "Order Rejected", "suggestedBooks": []}
    
    responses[order_id] = None
    response_locks[order_id] = threading.Event()

    threading.Thread(target=callVerifyTransaction, args=[order_id]).start() #call Function that 

    if response_locks[order_id].wait(timeout=5):  # Adjust timeout as needed
        response = responses.pop(order_id)
    else:
        print("---No response in 5 seconds for OrderID:", order_id)
        return {"orderId": order_id, "status": "Order Rejected", "suggestedBooks": []}
    
    if response["status"] == "Order Rejected":
        deleteId(order_id)
    else:
        with grpc.insecure_channel("order_queue:50055") as channel:
            stub = order_queue_grpc.OrderQueueServiceStub(channel)
            enqueue_order_request = order_queue.QueueOrderRequest(
                info=order.ExecInfo(id = order_id),
                booksInCart=Ordered_Books,
                name=request_data.get("name"),
                CreditCard=Credit_Card,
                BillingAddress=Billing_Address
            )
            enqueue_response = stub.EnqueueOrder(enqueue_order_request)
    
    if enqueue_response.error:
        print("---Error enqueuing order---")
        deleteId(order_id)
        return {"orderId": order_id, "status": "Order Rejected", "suggestedBooks": []}
    
    order_status_response = {
        "orderId": order_id,
        "status": response["status"],
        "suggestedBooks": response["suggestedBooks"],
    }
    #Return the response

    return order_status_response

@app.route('/callback', methods=['POST'])
def callback():
    """Receives responses from microservices."""
    response_data = request.json
    request_id = response_data.get("id")
    responses[request_id] = response_data
    response_locks[request_id].set()  # Notify waiting thread
        

    return jsonify({"status": "received"})


if __name__ == "__main__":
    # Run the app in debug mode to enable hot reloading.
    # This is useful for development.
    # The default port is 5000.
    app.run(host="0.0.0.0")
