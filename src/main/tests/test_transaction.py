import unittest
from src.models.transactionModel import Transaction  # Assuming Transaction model is defined in transactionModel
from src.utils.validator import Validator

class TestTransaction(unittest.TestCase):
    def setUp(self):
        """Set up test variables."""
        self.validator = Validator()
        self.valid_transaction_data = {
            'amount': 100.0,
            'currency': 'USD',
            'sender_id': 'user_1',
            'receiver_id': 'user_2'
        }
        self.invalid_transaction_data = {
            'amount': 'not_a_number',
            'currency': '',
            'sender_id': None,
            'receiver_id': None
        }

    def test_transaction_creation_valid(self):
        """Test creating a transaction with valid data."""
        transaction = Transaction(**self.valid_transaction_data)
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.amount, self.valid_transaction_data['amount'])
        self.assertEqual(transaction.currency, self.valid_transaction_data['currency'])

    def test_transaction_creation_invalid(self):
        """Test creating a transaction with invalid data."""
        with self.assertRaises(ValueError):
            Transaction(**self.invalid_transaction_data)

    def test_transaction_amount_validation(self):
        """Test amount validation."""
        self.assertTrue(self.validator.is_float(self.valid_transaction_data['amount']))
        self.assertFalse(self.validator.is_float(self.invalid_transaction_data['amount']))

    def test_transaction_currency_validation(self):
        """Test currency validation."""
        valid_currencies = ['USD', 'EUR', 'GBP']
        self.assertTrue(self.validator.is_in_list(self.valid_transaction_data['currency'], valid_currencies))
        self.assertFalse(self.validator.is_in_list(self.invalid_transaction_data['currency'], valid_currencies))

if __name__ == '__main__':
    unittest.main()
