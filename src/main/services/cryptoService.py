import requests
import logging
import hashlib
import json
from datetime import datetime
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CryptoService:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.cryptoexchange.com/v1"  # Example API endpoint

    def generate_key_pair(self):
        """Generate a new RSA key pair for secure transactions."""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        return private_key, public_key

    def sign_transaction(self, private_key, transaction_data):
        """Sign a transaction using the private key."""
        transaction_json = json.dumps(transaction_data, sort_keys=True).encode()
        signature = private_key.sign(
            transaction_json,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature

    def create_transaction(self, sender, recipient, amount):
        """Create a new cryptocurrency transaction."""
        transaction_data = {
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "timestamp": datetime.utcnow().isoformat()
        }
        logging.info(f"Creating transaction: {transaction_data}")
        return transaction_data

    def broadcast_transaction(self, transaction_data):
        """Broadcast the transaction to the blockchain network."""
        try:
            response = requests.post(f"{self.base_url}/transactions", json=transaction_data, headers={
                "API-Key": self.api_key,
                "Content-Type": "application/json"
            })
            response.raise_for_status()
            logging.info("Transaction broadcasted successfully.")
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error broadcasting transaction: {e}")
            return None

    def get_transaction_status(self, transaction_id):
        """Get the status of a transaction."""
        try:
            response = requests.get(f"{self.base_url}/transactions/{transaction_id}", headers={
                "API-Key": self.api_key
            })
            response.raise_for_status()
            logging.info(f"Transaction status retrieved: {response.json()}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error retrieving transaction status: {e}")
            return None

    def hash_transaction(self, transaction_data):
        """Generate a hash for the transaction data."""
        transaction_json = json.dumps(transaction_data, sort_keys=True).encode()
        transaction_hash = hashlib.sha256(transaction_json).hexdigest()
        logging.info(f"Transaction hash generated: {transaction_hash}")
        return transaction_hash

# Example usage
if __name__ == "__main__":
    api_key = "your_api_key"
    api_secret = "your_api_secret"
    
    crypto_service = CryptoService(api_key, api_secret)
    
    # Generate key pair
    private_key, public_key = crypto_service.generate_key_pair()
    
    # Create a transaction
    transaction = crypto_service.create_transaction("sender_address", "recipient_address", 0.01)
    
    # Sign the transaction
    signature = crypto_service.sign_transaction(private_key, transaction)
    
    # Hash the transaction
    transaction_hash = crypto_service.hash_transaction(transaction)
    
    # Broadcast the transaction
    transaction_response = crypto_service.broadcast_transaction(transaction)
    
    # Check transaction status
    if transaction_response:
        transaction_id = transaction_response.get("id")
        status = crypto_service.get_transaction_status(transaction_id)
