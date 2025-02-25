import unittest
import requests

class TestUserFunctionality(unittest.TestCase):
    BASE_URL = "http://localhost:5000"  # Change this to your application's base URL

    def setUp(self):
        # This method will run before each test
        self.test_user = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "securepassword"
        }

    def test_user_registration(self):
        """Test user registration functionality."""
        response = requests.post(f"{self.BASE_URL}/api/register", json=self.test_user)
        self.assertEqual(response.status_code, 201)
        self.assertIn("user_id", response.json())

    def test_user_login(self):
        """Test user login functionality."""
        response = requests.post(f"{self.BASE_URL}/api/login", json={
            "email": self.test_user["email"],
            "password": self.test_user["password"]
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())

    def test_user_profile(self):
        """Test fetching user profile after login."""
        login_response = requests.post(f"{self.BASE_URL}/api/login", json={
            "email": self.test_user["email"],
            "password": self.test_user["password"]
        })
        token = login_response.json()["token"]

        headers = {"Authorization": f"Bearer {token}"}
        profile_response = requests.get(f"{self.BASE_URL}/api/profile", headers=headers)
        self.assertEqual(profile_response.status_code, 200)
        self.assertEqual(profile_response.json()["email"], self.test_user["email"])

    def tearDown(self):
        # This method will run after each test
        # Clean up test user if necessary
        requests.delete(f"{self.BASE_URL}/api/users/{self.test_user['email']}")  # Adjust as necessary

if __name__ == "__main__":
    unittest.main()
