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
import suggestions.suggestions_pb2 as suggestions
import suggestions.suggestions_pb2_grpc as suggestions_grpc
import shared.order_pb2 as order
import shared.order_pb2_grpc as order_grpc

import grpc
from concurrent import futures


# Create a class to define the server functions, derived from
# fraud_detection_pb2_grpc.HelloServiceServicer
class SuggestionService(suggestions_grpc.SuggestionsServiceServicer):
    # Create an RPC function to say hello
    orders = {}
    svc_idx = 2
    def InitGetSuggestions(self, request, context):
        print("---suggestions initalized---")
        self.orders[request.info.id] = {"vc": request.info.vectorClock, "books": request.booksInCart, 'lock': threading.Lock()}
        response = order.ErrorResponse(error = False)
        return response
    
    def merge(self, local_vc, incoming_vc):
        for i in range(3):
            local_vc[i] = max(local_vc[i], incoming_vc[i])
    
    def increment(self, local_vc):
        local_vc[self.svc_idx] +=1
        
    def GetSuggestions(self, request, context):
        # Create a SuggestionsResponse object
        print("-- suggestion service called --")
        response = order.ErrorResponse()
        entry = self.orders.get(request.id)
        if entry == None:
            print("--id already deleted--")
            response.error = False
            return response
        entry['lock'].acquire()
        self.merge(entry["vc"], request.vectorClock)
        
        if(entry["vc"][0] < 3 or entry["vc"][1] < 2 or entry["vc"][2] < 0):
            print("-- suggestion service called - waiting for process--")
            response.error = False
            entry['lock'].release()
            return response
        self.increment(entry["vc"])
        entry['lock'].release()
        all_books = [
            suggestions.Book(bookId=101, title="The Great Gatsby", author="F. Scott Fitzgerald"),
            suggestions.Book(bookId=102, title="1984", author="George Orwell"),
            suggestions.Book(bookId=103, title="To Kill a Mockingbird", author="Harper Lee"),
            suggestions.Book(bookId=104, title="Pride and Prejudice", author="Jane Austen"),
            suggestions.Book(bookId=105, title="Moby-Dick", author="Herman Melville"),
            suggestions.Book(bookId=106, title="War and Peace", author="Leo Tolstoy"),
            suggestions.Book(bookId=107, title="The Catcher in the Rye", author="J.D. Salinger"),
            suggestions.Book(bookId=108, title="The Hobbit", author="J.R.R. Tolkien"),
        ]
        suggested_books = random.sample(all_books, 3)
        
        self.sendToOrchestrator(request.id, suggested_books)

        # Return the response object
        response.error = False
        return response
    
    def DeleteOrder(self, request, context):
        print(f"--deleting id: {request.id}--")
        self.orders.pop(request.id, None)
        response = order.ErrorResponse()
        response.error = False
        return response

    def sendToOrchestrator(self, id, books):
        orchestrator_url ='http://orchestrator:5000/callback'
        suggested_books = []
        for book in books:
            suggested_books.append(
                {"bookId": book.bookId, "title": book.title, "author": book.author}
            )
        order_status_response = {
            "id": id,
            "status": "Order Approved",
            "suggestedBooks": suggested_books,
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


def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add SuggestionService
    suggestions_grpc.add_SuggestionsServiceServicer_to_server(
        SuggestionService(), server
    )
    # Listen on port 50051
    port = "50053"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print("Suggestion server started. Listening on port 50053.")
    # Keep thread alive
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
