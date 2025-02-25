import os
import json
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class SecretsManager:
    def __init__(self, key=None):
        # Generate a new key if none is provided
        if key is None:
            self.key = self.generate_key()
        else:
            self.key = key
        self.cipher = Fernet(self.key)

    @staticmethod
    def generate_key():
        """Generate a new encryption key."""
        return Fernet.generate_key()

    def encrypt(self, data):
        """Encrypt sensitive data."""
        if isinstance(data, str):
            data = data.encode()  # Convert string to bytes
        encrypted_data = self.cipher.encrypt(data)
        return encrypted_data

    def decrypt(self, encrypted_data):
        """Decrypt sensitive data."""
        decrypted_data = self.cipher.decrypt(encrypted_data)
        return decrypted_data.decode()  # Convert bytes back to string

    def save_key(self, filename='secret.key'):
        """Save the encryption key to a file."""
        with open(filename, 'wb') as key_file:
            key_file.write(self.key)

    @staticmethod
    def load_key(filename='secret.key'):
        """Load the encryption key from a file."""
        return open(filename, 'rb').read()

    def store_secret(self, secret_name, secret_value):
        """Store a secret in a JSON file."""
        encrypted_value = self.encrypt(secret_value)
        secrets = {}
        
        # Load existing secrets if the file exists
        if os.path.exists('secrets.json'):
            with open('secrets.json', 'r') as f:
                secrets = json.load(f)

        secrets[secret_name] = encrypted_value.decode()  # Store as string
        with open('secrets.json', 'w') as f:
            json.dump(secrets, f)

    def retrieve_secret(self, secret_name):
        """Retrieve a secret from the JSON file."""
        if not os.path.exists('secrets.json'):
            raise FileNotFoundError("Secrets file not found.")

        with open('secrets.json', 'r') as f:
            secrets = json.load(f)

        if secret_name not in secrets:
            raise KeyError(f"Secret '{secret_name}' not found.")

        encrypted_value = secrets[secret_name].encode()  # Convert to bytes
        return self.decrypt(encrypted_value)

# Example usage
if __name__ == "__main__":
    # Initialize SecretsManager
    secrets_manager = SecretsManager()

    # Generate and save a new key (only do this once)
    # secrets_manager.save_key()

    # Store a secret
    secrets_manager.store_secret('API_KEY', os.getenv('API_KEY'))

    # Retrieve a secret
    try:
        api_key = secrets_manager.retrieve_secret('API_KEY')
        print(f"Retrieved API Key: {api_key}")
    except Exception as e:
        print(f"Error: {e}")
