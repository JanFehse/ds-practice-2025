from copy import deepcopy
from locust import HttpUser, task, between

#host = "http://local:8081"

books = [
    {"name": "Book A", "quantity": 1},
    {"name": "Book B", "quantity": 1},
]

credit_cards = [
    {"number": "4111111111111111", 
                   "expirationDate": "12/25", 
                   "cvv": "123"},
    {"number": "3334111111111111111", 
                   "expirationDate": "12/25", 
                   "cvv": "123"}
]

orderdata = {
    "items" : books,
    "user": {
        "name": "John Doe",
        "contact": "john.doe@example.com"},
    "userComment": "Please handle with care.",
    "billingAddress": {
        "street": "Raatuse", 
        "city": "Tartu", 
        "state": "Tartu", 
        "zip": "1234", 
        "country": "Estonia"
    },
    "shippingMethod": "Standard",
    "giftWrapping": True,
    "termsAndConditionsAccepted": True,  
}

#Multiple non-fraudulent non-conflicting orders
class Multiple_non_Fraudulent(HttpUser):
    wait_time = between(2,4)

    def send_order(self, orderData):
        with self.client.post("/checkout", json=orderData, catch_response=True) as response:
            print("\n--- Response Status Code:", response.status_code)
            print("--- Response Body:", response.text)
            data = response.json()
            
            if response.status_code != 200:
                response.failure("Failed order submission")
            elif data.get("status") == "Order Rejected":
                response.failure("Order Rejected")
            else:
                response.success()

    @task
    def non_fradulent_one(self):
        data = deepcopy(orderdata)
        data['items'] = [books[0]]
        data['creditCard'] = credit_cards[0]
        self.send_order(data)

    @task
    def non_fradulent_two(self):
        data = deepcopy(orderdata)
        data['items'] = [books[1]]
        data['creditCard'] = credit_cards[0]
        self.send_order(data)
    
    @task
    def non_fradulent_three(self):
        data = deepcopy(orderdata)
        data['items'] = [books[0]]
        data['creditCard'] = credit_cards[0]
        self.send_order(data)


#Multiple mixed orders
class Multiple_mixed(HttpUser):
    wait_time = between(2,4)

    def send_order(self, orderData):
        with self.client.post("/checkout", json=orderData, catch_response=True) as response:
            print("\n--- Response Status Code:", response.status_code)
            print("--- Response Body:", response.text)
            data = response.json()
            
            if response.status_code != 200:
                response.failure("Failed order submission")
            elif data.get("status") == "Order Rejected":
                response.failure("Order Rejected")
            else:
                response.success()

    @task
    def non_fradulent_one(self):
        data = deepcopy(orderdata)
        data['items'] = [books[0]]
        data['creditCard'] = credit_cards[0]
        self.send_order(data)

    @task
    def non_fradulent_two(self):
        data = deepcopy(orderdata)
        data['items'] = [books[1]]
        data['creditCard'] = credit_cards[0]
        self.send_order(data)
    
    @task
    def fradulent_one(self):
        data = deepcopy(orderdata)
        data['items'] = [books[0]]
        data['creditCard'] = credit_cards[1]
        self.send_order(data)
    

#Conflicting orders:
#many orders of the same book
class Conflicting_orders(HttpUser):
    def send_order(self, orderData):
        with self.client.post("/checkout", json=orderData, catch_response=True) as response:
            print("\n--- Response Status Code:", response.status_code)
            print("--- Response Body:", response.text)
            data = response.json()
            
            if response.status_code != 200:
                response.failure("Failed order submission")
            elif data.get("status") == "Order Rejected":
                response.failure("Order Rejected")
            else:
                response.success()

    @task
    def non_fradulent_one(self):
        data = deepcopy(orderdata)
        data['items'] = [books[0]]
        data['creditCard'] = credit_cards[0]
        self.send_order(data)

    @task
    def non_fradulent_two(self):
        data = deepcopy(orderdata)
        data['items'] = [books[0]]
        data['creditCard'] = credit_cards[0]
        self.send_order(data)
 