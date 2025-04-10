**Architecture**

The system employs a microservices-based architecture with clearly delineated responsibilities for each component. The Frontend acts as the user interface, enabling users to submit orders. These orders are transmitted to the Orchestrator, which serves as the central coordinating entity.

**Communication**

Communication commences with the Frontend sending an order request to the Orchestrator, which then disseminates the relevant data to all necessary microservices. Once initialization procedures are concluded, the Orchestrator initiates order processing by invoking the Transaction Verification service. Following successful verification, the Suggestions service informs the Orchestrator of the completed order, identified by a unique order ID. Subsequently, the Orchestrator places the order into an Order Queue, from which Executors retrieve and store the order data.

**Timing**

Inter-service communication within this architecture is designed to be partially asynchronous, thus enabling components to operate independently without causing system blockage. Execution times are bounded, ensuring predictable system performance.

**Failure**

Regarding fault tolerance, Executors are explicitly designed to be the only components susceptible to failure, specifically limited to crash-stop scenarios. In the event of an Executor’s failure, remaining Executors seamlessly compensate by processing the outstanding orders in the queue, thereby maintaining system resilience and ensuring uninterrupted service continuity. The architecture assumes the absence of malicious activities and excludes the possibility of arbitrary faults.
