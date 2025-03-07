import random
import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if "__file__" in globals() else os.getenv("PYTHONFILE", "")
grpc_path = os.path.abspath(os.path.join(FILE, "../../../utils/pb"))
sys.path.insert(0, grpc_path)
import suggestions.suggestions_pb2 as suggestions
import suggestions.suggestions_pb2_grpc as suggestions_grpc

import grpc
from concurrent import futures


# Create a class to define the server functions, derived from
# fraud_detection_pb2_grpc.HelloServiceServicer
class SuggestionService(suggestions_grpc.SuggestionsServiceServicer):
    # Create an RPC function to say hello
    def GetSuggestions(self, request, context):
        # Create a SuggestionsResponse object
        print("-- suggestion service called --")

        response = suggestions.SuggestionsResponse()
        # for book in request.booksInCart:
        #    print(f"Book in Cart: {book.title} by {book.author}")
        # Set the booksSuggested field of the response object
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
        response = suggestions.SuggestionsResponse(booksSuggested=suggested_books)

        # Print the suggested books
        # for book in response.booksSuggested:
        # print(f"Suggested Book: {book.title} by {book.author}")

        # Return the response object
        return response


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
