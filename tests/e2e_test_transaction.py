import unittest
import requests

class TestTransactionFunctionality(unittest.TestCase):
    BASE_URL = "http://localhost:5000"  # Change this to your application's base URL

    def setUp(self):
        # This method will run before each test
        self.test_user = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "securepassword"
        }
        self.test_transaction = {
            "recipient": "recipient_address",
            "amount": 0.01
        }

        # Register and log in the test user
        requests.post(f"{self.BASE_URL}/api/register", json=self.test_user)
        login_response = requests.post(f"{self.BASE_URL}/api/login", json={
            "email": self.test_user["email"],
            "password": self.test_user["password"]
        })
        self.token = login_response.json()["token"]

    def test_create_transaction(self):
        """Test creating a new transaction."""
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(f"{self.BASE_URL}/api/transactions", json=self.test_transaction, headers=headers)
        self.assertEqual(response.status_code, 201)
        self.assertIn("transaction_id", response.json())

    def test_view_transaction_history(self):
        """Test viewing transaction history."""
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(f"{self.BASE_URL}/api/transactions", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)  # Expecting a list of transactions

    def tearDown(self):
        # This method will run after each test
        # Clean up test user and transactions if necessary
        requests.delete(f"{self.BASE_URL}/api/users/{self.test_user['email']}")  # Adjust as necessary

if __name__ == "__main__":
    unittest.main()
