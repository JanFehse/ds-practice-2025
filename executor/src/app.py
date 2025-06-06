import sys
import os
import time
import socket
import threading
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
from google.protobuf.empty_pb2 import Empty

from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

resource = Resource.create(attributes={
        SERVICE_NAME: "executor"
    })

tracerProvider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="observability:4317", insecure=True))
tracerProvider.add_span_processor(processor)
trace.set_tracer_provider(tracerProvider)

reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="observability:4317", insecure=True)
)
meterProvider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(meterProvider)

tracer = trace.get_tracer("executor.tracer")
meter = metrics.get_meter("executor.meter")


# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if "__file__" in globals() else os.getenv("PYTHONFILE", "")
grpc_path = os.path.abspath(os.path.join(FILE, "../../../utils/pb"))
sys.path.insert(0, grpc_path)
import shared.order_pb2 as order
import shared.order_pb2_grpc as order_grpc
import executor.executor_pb2 as executor
import executor.executor_pb2_grpc as executor_grpc
import order_queue.order_queue_pb2 as order_queue
import order_queue.order_queue_pb2_grpc as order_queue_grpc
import payment.payment_pb2 as payment
import payment.payment_pb2_grpc as payment_grpc
import database.database_pb2 as database
import database.database_pb2_grpc as database_grpc

import grpc

# Create a class to define the server functions
@tracer.start_as_current_span("process_order")
class ExecutorService(executor_grpc.ExecutorServiceServicer):
    wait_time = 5
    executors = []
    lastToken = time.time()
    myip = socket.gethostbyname(socket.gethostname())

    def __init__(self):
        time.sleep(1)
        self.ElectLeader(Empty(), Empty())
        threading.Thread(target=self.checkToken, args=[]).start()
        
        meter.create_observable_gauge(
        name="amount.executors.Executor",
        description="The amount of running executors",
        callbacks=[self.executor_number_callback],
        unit="integer")
        return

    def executor_number_callback(self, result):
        return [metrics.Observation(len(self.executors))]
    
    def ElectLeader(self, request, context):
        #myip = socket.gethostbyname(socket.gethostname())
        with grpc.insecure_channel("order_queue:50055") as channel:
            stub = order_queue_grpc.OrderQueueServiceStub(channel)
            request = order_queue.CoordinateRequest(portnumber=self.myip)
            response = stub.CoordinateExecutors(request)
        self.executors = list(response.ids)
        self.lastToken = time.time()
        if self.executors.index(self.myip) == 0:
            self.pass_token()
        return Empty()

    def checkToken(self):
        while time.time() - self.lastToken <= self.wait_time*(len(self.executors) + 1):
            time.sleep(self.wait_time*(len(self.executors) + 1))
        #heartbeat your predecessor
        predecessor = (self.executors.index(self.myip) + len(self.executors) - 1) % len(self.executors)
        try: 
            with grpc.insecure_channel(self.executors[predecessor]+":50061") as channel:
                stub = executor_grpc.ExecutorServiceStub(channel)
                print("Pinging ", self.executors[predecessor])
                response = stub.Ping(Empty())
        except Exception as e:
                print("error pinging", self.executors[predecessor], " Starting new leader election")
                with grpc.insecure_channel("order_queue:50055") as channel:
                    stub = order_queue_grpc.OrderQueueServiceStub(channel)
                    stub.NewElection(Empty())      
        self.lastToken = time.time()
        threading.Thread(target=self.checkToken, args=[]).start()
        return
    
    def Ping(self, request, context):
        print("Pong")
        response = order.ErrorResponse()
        response.error = False
        return response
    

    receive_token_counter = meter.create_counter(
    "receivedtoken.counter", unit="1", description="Counts the amount of times token is received"
    )
    def ReceiveToken(self, request, context):
        threading.Thread(target=self.pass_token, args=[]).start()
        #print("--received token--")
        self.lastToken = time.time()
        self.receive_token_counter.add(1, {"ip": self.myip})
        response = order.ErrorResponse(error=False)
        return response
    
    def pass_token(self):
        with grpc.insecure_channel("order_queue:50055") as channel:
            stub = order_queue_grpc.OrderQueueServiceStub(channel)
            order_response = stub.DequeueOrder(Empty())
        if not order_response.HasField("order"):
            #print("No new order in queue")
            time.sleep(self.wait_time)
        else:
            threading.Thread(target=self.process_order, args=[order_response]).start()
        start = (self.executors.index(self.myip) + 1) % len(self.executors)
        had_error = True
        while had_error:
            try: 
                with grpc.insecure_channel(self.executors[start]+":50061") as channel:
                    stub = executor_grpc.ExecutorServiceStub(channel)
                    #print("Passing Token to", self.executors[start])
                    pass_response = stub.ReceiveToken(Empty())
                    if not pass_response.error:
                        had_error = False
                    else:
                        raise Exception('ErrorResponse')
            except Exception as e:
                print("error passing token to", self.executors[start])        
                start = (start + 1) % len(self.executors)
        return
    
    def process_order(self, existingOrder):
        order_id = existingOrder.order.info.id
        print("processing order with id: ", order_id)
        #two phase commit
        ready_votes = []
        payment_prepare_request = payment.PrepareRequestPayment(name = existingOrder.order.name, 
                                        CreditCard = existingOrder.order.CreditCard,
                                        BillingAddress=  existingOrder.order.BillingAddress,
                                        price= 10, 
                                        id= order_id)
        
        changeamountrequests = []
        total_amount = 0
        for book in existingOrder.order.booksInCart:
            change_request = database.ChangeAmountRequest(title = book.title, amount = book.quantity)
            total_amount += book.quantity
            changeamountrequests.append(change_request)
        database_prepare_request = database.PrepareRequestDatabase(id = order_id, books = changeamountrequests)

        try:
            with grpc.insecure_channel("payment_service:50056") as channel:
                stub = payment_grpc.PaymentServiceStub(channel)
                payment_response = stub.Prepare(payment_prepare_request)
                ready_votes.append(not payment_response.error)
        except Exception as e:
            print(e)
            ready_votes.append(False)

        try:
            with grpc.insecure_channel("primarydatabase:50057") as channel:
                stub = database_grpc.DatabaseServiceStub(channel)
                database_response = stub.Prepare(database_prepare_request)
                ready_votes.append(not database_response.error)
        except Exception as e:
            print(e)
            ready_votes.append(False)

        info = order.ExecInfo(id = order_id, vectorClock = [0,0,0])
        
        if all(ready_votes):
            with grpc.insecure_channel("payment_service:50056") as channel:
                stub = payment_grpc.PaymentServiceStub(channel)
                payment_response = stub.Commit(info)
            with grpc.insecure_channel("primarydatabase:50057") as channel:
                stub = database_grpc.DatabaseServiceStub(channel)
                database_response = stub.Commit(info)
            print(f"All services Commited for id: {order_id}")
        else: 
            with grpc.insecure_channel("payment_service:50056") as channel:
                stub = payment_grpc.PaymentServiceStub(channel)
                payment_response = stub.Abort(info)
            with grpc.insecure_channel("primarydatabase:50057") as channel:
                stub = database_grpc.DatabaseServiceStub(channel)
                database_response = stub.Abort(info)
            print(f"Transaction with id {order_id} Aborted")


def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    executor_grpc.add_ExecutorServiceServicer_to_server(
        ExecutorService(), server
    )
    # Listen on port 50051
    port = "50061"
    server.add_insecure_port("[::]:" + port)
    # Start the server
    server.start()
    print("Order Queue server started. Listening on port 50060.")
    # Keep thread alive
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
