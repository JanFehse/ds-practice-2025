from locust import HttpUser, task

books = [
    {"name": "Book A", "quantity": 1},
    {"name": "Book B", "quantity": 1},
]

orderdata = {
    "items" : books,
    "user": {
        "name": "John Doe",
        "contact": "john.doe@example.com",
    },
    "creditCard": {"number": "33334111111111111111", 
                   "expirationDate": "12/25", 
                   "cvv": "123"},
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

class Test(HttpUser):
    @task
    def single_non_fradulent(self):
        with self.client.post("/checkout", json=orderdata, catch_response=True) as response:
            print("\n--- Response Status Code:", response.status_code)
            print("--- Response Body:", response.text)
            data = response.json()
            
            if response.status_code != 200:
                response.failure("Failed order submission")
            elif data.get("status") == "Order Rejected":
                response.failure("Order Rejected")
            else:
                response.success()