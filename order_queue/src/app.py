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
import psutil

from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

resource = Resource.create(attributes={
        SERVICE_NAME: "order_queue"
    })

reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="observability:4317", insecure=True)
)
meterProvider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(meterProvider)

meter = metrics.get_meter("order_queue.meter")


# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if "__file__" in globals() else os.getenv("PYTHONFILE", "")
grpc_path = os.path.abspath(os.path.join(FILE, "../../../utils/pb"))
sys.path.insert(0, grpc_path)
import shared.order_pb2 as order
import shared.order_pb2_grpc as order_grpc
import order_queue.order_queue_pb2 as order_queue
import order_queue.order_queue_pb2_grpc as order_queue_grpc
import executor.executor_pb2 as executor
import executor.executor_pb2_grpc as executor_grpc


premium_user = {"Fehse", "Eulering", "Beyerle", "Einstein", "Hawking", "Newton", "Curie", "Feynman", "Bohr", "Planck"}

# Create a class to define the server functions
class OrderQueueService(order_queue_grpc.OrderQueueServiceServicer):
    # initialize the class
    def __init__(self):
        self.orders = []
        self.executors = []
        meter.create_observable_gauge(
        name="cpu.usage.OrderQueue",
        description="the real-time CPU clock speed",
        callbacks=[self.cpu_frequency_callback],
        unit="Percent")

    def cpu_frequency_callback(self, result):
        return [metrics.Observation(psutil.cpu_percent(interval=1))]
    
    #Initialize into orders
    queue_length_counter = meter.create_up_down_counter(
    "queue.length.counter", unit="1", description="Counts the length of the queue"
    )
    def EnqueueOrder(self, request, context):
        heapq.heappush(self.orders, (self._get_priority(request), request))
        response = order.ErrorResponse()
        response.error = False
        print("---Order Enqueued---")
        self.queue_length_counter.add(1)
        return response
    
    def DequeueOrder(self, request, context):
        if self.orders:
            _, deq_order = heapq.heappop(self.orders)
            print(f"---Order {deq_order.info.id} dequeued---")
            response = order_queue.DequeueOrderResponse(order=deq_order)
            self.queue_length_counter.add(-1)
        else:
            error = order.ErrorResponse()
            error.error = True
            response = order_queue.DequeueOrderResponse(error=error)
            #print("---No order or dequeueing available---")
        return response
    
    def CoordinateExecutors(self, request, context):
        idExecutor = request.portnumber
        self.executors.append(idExecutor)
        time.sleep(2)
        response = order_queue.CoordinateResponse(ids=self.executors)
        return response
    
    def _get_priority(self, order):
        is_premium = order.name in premium_user
        num_books = sum(book.quantity for book in order.booksInCart)
        # negative value for max heap
        return (-int(is_premium), -num_books, time.time())
    
    def NewElection(self, request, context):
        print("New Election called")
        exec_local = copy.deepcopy(self.executors)
        self.executors = []
        for exec in exec_local:
            #Call all old executors in parrallel to start the election
            threading.Thread(target=self.electionAtExecutor, args=[exec]).start()
        return Empty()
    
    def electionAtExecutor(self, exec):
        try:
            with grpc.insecure_channel(exec+":50061") as channel:
                stub = executor_grpc.ExecutorServiceStub(channel)
                print("Elect Leader calling at ", exec)
                stub.ElectLeader(Empty())
        except:
            print(exec, "died")
        return
    

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor())
    # Add HelloService
    order_queue_grpc.add_OrderQueueServiceServicer_to_server(
        OrderQueueService(), server
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
