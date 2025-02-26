import hashlib
import json
import numpy as np
import logging
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from cryptography.fernet import Fernet

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AnomalyDetector:
    """Class to detect anomalies in KYC data."""
    def __init__(self, data):
        self.data = data
        self.isolation_forest = IsolationForest(contamination=0.1)
        self.random_forest = RandomForestClassifier()

    def train_model(self):
        """Train the anomaly detection models."""
        self.isolation_forest.fit(self.data)
        # For Random Forest, we need labeled data (0: normal, 1: anomaly)
        labels = np.array([0] * (len(self.data) - 1) + [1])  # Last entry is an anomaly
        self.random_forest.fit(self.data, labels)

    def detect_anomalies(self):
        """Detect anomalies in the data using both models."""
        isolation_predictions = self.isolation_forest.predict(self.data)
        rf_predictions = self.random_forest.predict(self.data)
        anomalies = np.where((isolation_predictions == -1) | (rf_predictions == 1))[0]
        return anomalies

class BlockchainIdentity:
    """Class to manage identity on a mock blockchain."""
    def __init__(self):
        self.identities = {}

    def register_identity(self, user_id, data):
        """Register a new identity."""
        identity_hash = self.create_identity_hash(data)
        self.identities[user_id] = identity_hash
        logging.info(f"Identity registered for {user_id}: {identity_hash}")

    def verify_identity(self, user_id, data):
        """Verify an identity using the hash."""
        identity_hash = self.create_identity_hash(data)
        if user_id in self.identities and self.identities[user_id] == identity_hash:
            logging.info(f"Identity verified for {user_id}.")
            return True
        else:
            logging.warning(f"Identity verification failed for {user_id}.")
            return False

    def create_identity_hash(self, data):
        """Create a hash of the identity data."""
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

class DataEncryption:
    """Class to handle data encryption and decryption."""
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt_data(self, data):
        """Encrypt the data."""
        return self.cipher.encrypt(json.dumps(data).encode())

    def decrypt_data(self, encrypted_data):
        """Decrypt the data."""
        return json.loads(self.cipher.decrypt(encrypted_data).decode())

# Example usage
if __name__ == "__main__":
    # Sample KYC data (features could be age, income, etc.)
    kyc_data = np.array([[25, 50000], [30, 60000], [35, 70000], [40, 80000], [100, 1000000]])  # Last entry is an anomaly

    # Anomaly detection
    detector = AnomalyDetector(kyc_data)
    detector.train_model()
    anomalies = detector.detect_anomalies()
    logging.info(f"Detected anomalies at indices: {anomalies}")

    # Blockchain identity management
    blockchain = BlockchainIdentity()
    user_id = "user123"
    user_data = {"name": "Alice", "age": 30, "income": 60000}

    # Register identity
    blockchain.register_identity(user_id, user_data)

    # Verify identity
    verification_result = blockchain.verify_identity(user_id, user_data)

    # Data encryption example
    data_encryption = DataEncryption()
    encrypted_data = data_encryption.encrypt_data(user_data)
    logging.info(f"Encrypted user data: {encrypted_data}")

    decrypted_data = data_encryption.decrypt_data(encrypted_data)
    logging.info(f"Decrypted user data: {decrypted_data}")
