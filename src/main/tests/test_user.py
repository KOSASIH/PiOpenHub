import unittest
from src.models.userModel import User  # Assuming User model is defined in userModel
from src.utils.validator import Validator

class TestUser(unittest.TestCase):
    def setUp(self):
        """Set up test variables."""
        self.validator = Validator()
        self.valid_user_data = {
            'username': 'test_user',
            'email': 'test_user@example.com',
            'phone': '+1234567890',
            'age': 25
        }
        self.invalid_user_data = {
            'username': '',
            'email': 'invalid_email',
            'phone': '12345',
            'age': 'not_a_number'
        }

    def test_user_creation_valid(self):
        """Test creating a user with valid data."""
        user = User(**self.valid_user_data)
        self.assertIsNotNone(user)
        self.assertEqual(user.username, self.valid_user_data['username'])
        self.assertEqual(user.email, self.valid_user_data['email'])

    def test_user_creation_invalid(self):
        """Test creating a user with invalid data."""
        with self.assertRaises(ValueError):
            User(**self.invalid_user_data)

    def test_user_email_validation(self):
        """Test email validation."""
        self.assertTrue(self.validator.is_email(self.valid_user_data['email']))
        self.assertFalse(self.validator.is_email(self.invalid_user_data['email']))

    def test_user_phone_validation(self):
        """Test phone validation."""
        self.assertTrue(self.validator.is_phone(self.valid_user_data['phone']))
        self.assertFalse(self.validator.is_phone(self.invalid_user_data['phone']))

    def test_user_age_validation(self):
        """Test age validation."""
        self.assertTrue(self.validator.is_integer(self.valid_user_data['age']))
        self.assertFalse(self.validator.is_integer(self.invalid_user_data['age']))

if __name__ == '__main__':
    unittest.main()
