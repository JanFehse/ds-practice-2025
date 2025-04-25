import sys
import os
import time
import grpc
import heapq
import copy
import threading
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
from google.protobuf.empty_pb2 import Empty

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if "__file__" in globals() else os.getenv("PYTHONFILE", "")
grpc_path = os.path.abspath(os.path.join(FILE, "../../../utils/pb"))
sys.path.insert(0, grpc_path)
import shared.order_pb2 as order
import shared.order_pb2_grpc as order_grpc
import database.databse_pb2 as database
import database.order_pb2_grpc as database_grpc


# Create a class to define the server functions
class DatabaseService(database_grpc.DatabaseServiceServicer):
    # initialize the class
    def __init__(self):
        self.store = {}
    
    def call_primary(self):
        #TODO
        print("calling primary")
        return
    
    def Read(self, request, context):
        stock = self.store.get(request.title, 0)
        return database.ReadResponse(amount=stock)

    def Write(self, request, context):
        self.store[request.title] = request.new_stock
        return order.ErrorResponse(error=False)

    def Decrement(self, request, context):
        self.store[request.title] -= request.amount
        return order.ErrorResponse(error=False)
    
    def Increment(self, request, context):
        self.store[request.title] += request.amount
        return order.ErrorResponse(error=False)


class PrimaryDatabaseService(DatabaseService):
    
    backups = []
    
    def __init__(self, am_primary):
        super().__init__()
        self.locked_books = {}
        self.queuedCommits = {}
        if(not am_primary):
            self.call_primary()
            return
        time.sleep(5)
        return

    def Write(self, request, context):
        self.store[request.title] = request.new_stock
        self.updateBackups(request.title)
        return order.ErrorResponse(error=False)
        
    def Decrement(self, request, context):
        writeRequest = database.WriteRequest(title=request.title)
        writeRequest.new_stock = self.store[request.title] - request.amount
        self.Write(writeRequest, Empty())
        return order.ErrorResponse(error=False)
    
    def Increment(self, request, context):
        writeRequest = database.WriteRequest(title=request.title)
        writeRequest.new_stock = self.store[request.title] + request.amount
        self.Write(writeRequest, Empty())
        return order.ErrorResponse(error=False)

    def updateBackups(self, book):
        for backup in self.backups:
            try:
                #TODO define which port is used
                with grpc.insecure_channel(backup+":") as channel:
                    stub = database.DataBaseServiceStub(channel)
                    request = database.WriteRequest(title=book, new_stock=self.store[book])
                    pass_response = stub.Write(request)
                    if not pass_response.error:
                        had_error = False
                    else:
                        raise Exception('ErrorResponse')
            except Exception as e:
                print("Error updating ", backup)        
        return
    
    def Prepare(self,request,context):
        self.queuedCommits[request.id] = request.books
        for book in request.books:
            self.locked_books[book.title].acquire()
            if self.store[book.title] < book.amount:
                abortRequest = order.ExecInfo(id=request.id, vectorClock=[0,0,0])
                self.Abort(abortRequest, Empty())
                return order.ErrorResponse(error=True)
        print(f"Prepered DB for OrderID: {request.id}")
        return order.ErrorResponse(error=False)
    
    def Commit(self,request,context):
        for book in self.queuedCommits[request.id]:
            self.Decrement(book)
            self.locked_books[book.title].release()
        print(f"Commited to DB for OrderID: {request.id}")
        return order.ErrorResponse(error=False)
    
    def Abort(self,request,context):
        for book in self.queuedCommits[id]:
            self.locked_books[book.title].release()
        print(f"Aborted to DB for OrderID: {request.id}")
        response = order.ErrorResponse()
        response.error = True
        return response


def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    database_grpc.add_DatabaseServiceServicer_to_server(
        DatabaseService(), server
    )
    # Listen on port 50051
    port = "50055"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print("Order Queue server started. Listening on port 50055.")
    # Keep thread alive
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
