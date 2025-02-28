import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
suggestions_grpc_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/suggestions'))
sys.path.insert(0, suggestions_grpc_path)
import suggestions_pb2 as suggestions
import suggestions_pb2_grpc as suggestions_grpc

import grpc
from concurrent import futures

# Create a class to define the server functions, derived from
# fraud_detection_pb2_grpc.HelloServiceServicer
class SuggestionService(suggestions_grpc.SuggestionsServiceServicer):
    # Create an RPC function to say hello
    def GetSuggestions(self, request, context):
        # Create a SuggestionsResponse object
        response = suggestions.SuggestionsResponse()
        # Set the booksSuggested field of the response object
        suggested_books = [
            suggestions.Book(bookId=101, title="The Great Gatsby", author="F. Scott Fitzgerald"),
            suggestions.Book(bookId=102, title="1984", author="George Orwell"),
            suggestions.Book(bookId=103, title="To Kill a Mockingbird", author="Harper Lee")
        ]
        response = suggestions.SuggestionsResponse(booksSuggested=suggested_books)

        # Print the suggested books
        for book in response.booksSuggested:
            print(f"Suggested Book: {book.title} by {book.author}")

        # Return the response object
        return response

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add SuggestionService
    suggestions_grpc.add_SuggestionsServiceServicer_to_server(SuggestionService(), server)
    # Listen on port 50051
    port = "50053"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print("Server started. Listening on port 50053.")
    # Keep thread alive
    server.wait_for_termination()

if __name__ == '__main__':
    serve()