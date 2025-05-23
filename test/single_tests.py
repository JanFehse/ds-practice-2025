from copy import deepcopy
import unittest
import requests

BASE_URL = "http://localhost:8081/checkout"  # Replace with your actual server URL

class Test(unittest.TestCase):

    def setUp(self):
        self.valid_order = {
            "user": {
                "name": "John Doe",
                "contact": "john.doe@example.com"
            },
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
        self.books = [
            {"name": "Book A", "quantity": 1},
            {"name": "Book B", "quantity": 1},
            {"name": "Book A", "quantity": 13},
            {"name": "Book B", "quantity": 13},
        ]
        self.credit_cards = [
            {"number": "4111111111111111", 
                        "expirationDate": "12/25", 
                        "cvv": "123"},
            {"number": "3334111111111111111", 
                        "expirationDate": "12/25", 
                        "cvv": "123"}
        ]


    def send_order(self,orderData):
        response = requests.post(BASE_URL, json=orderData)
        
        self.assertEqual(response.status_code, 200)
        try:
            data = response.json()
            self.assertIn("status", data)
            self.assertNotEqual(data["status"], "Order Rejected")
        except ValueError:
            self.fail("Response is not valid JSON")
    
    def send_wrong_order(self,orderData):
        response = requests.post(BASE_URL, json=orderData)
        
        self.assertEqual(response.status_code, 200)
        try:
            data = response.json()
            self.assertIn("status", data)
            self.assertEqual(data["status"], "Order Rejected")
        except ValueError:
            self.fail("Response is not valid JSON")
    
    def test_valid_order(self):
        data = deepcopy(self.valid_order)
        data['items'] = [self.books[0]]
        data['creditCard'] = self.credit_cards[0]
        self.send_order(data)
    
    def test_to_many_books(self):
        data = deepcopy(self.valid_order)
        data['items'] = [self.books[2], self.books[3]]
        data['creditCard'] = self.credit_cards[0]
        self.send_order(data)

    def test_to_many_books_B(self):
        data = deepcopy(self.valid_order)
        data['items'] = [self.books[2]]
        data['creditCard'] = self.credit_cards[3]
        self.send_order(data)

    def test_wrong_creditCard(self):
        data = deepcopy(self.valid_order)
        data['items'] = [self.books[0]]
        data['creditCard'] = self.credit_cards[1]
        self.send_wrong_order(data)

if __name__ == '__main__':
    unittest.main()
