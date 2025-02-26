import hashlib
import time
import json

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = self.get_current_timestamp()
        self.transaction_id = self.calculate_transaction_id()

    def get_current_timestamp(self):
        """Return the current timestamp."""
        return int(time.time())

    def calculate_transaction_id(self):
        """Calculate a unique transaction ID based on the transaction details."""
        transaction_string = f"{self.sender}{self.recipient}{self.amount}{self.timestamp}".encode()
        return hashlib.sha256(transaction_string).hexdigest()

    def to_dict(self):
        """Convert the transaction to a dictionary for easy serialization."""
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'timestamp': self.timestamp,
            'transaction_id': self.transaction_id
        }

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)

class TransactionPool:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction):
        """Add a transaction to the pool."""
        if self.validate_transaction(transaction):
            self.transactions.append(transaction)
            return True
        return False

    def validate_transaction(self, transaction):
        """Validate a transaction before adding it to the pool."""
        # Basic validation checks
        if transaction.amount <= 0:
            print("Transaction amount must be positive.")
            return False
        if not transaction.sender or not transaction.recipient:
            print("Sender and recipient addresses must be valid.")
            return False
        # Additional checks can be added here (e.g., checking balances)
        return True

    def clear_transactions(self):
        """Clear the transaction pool."""
        self.transactions = []

    def get_transactions(self):
        """Return the list of pending transactions."""
        return self.transactions

# Example usage
if __name__ == "__main__":
    # Create a transaction pool
    transaction_pool = TransactionPool()

    # Create some transactions
    tx1 = Transaction(sender="Alice", recipient="Bob", amount=50)
    tx2 = Transaction(sender="Charlie", recipient="Dave", amount=100)

    # Add transactions to the pool
    transaction_pool.add_transaction(tx1)
    transaction_pool.add_transaction(tx2)

    # Print the transaction pool
    print("Current Transactions in Pool:")
    for tx in transaction_pool.get_transactions():
        print(tx)

    # Clear the transaction pool
    transaction_pool.clear_transactions()
    print("Transaction pool cleared.")
