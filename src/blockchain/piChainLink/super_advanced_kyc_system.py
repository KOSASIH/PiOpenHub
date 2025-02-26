import hashlib
import json
import numpy as np
from sklearn.ensemble import IsolationForest

class AnomalyDetector:
    """Class to detect anomalies in KYC data."""
    def __init__(self, data):
        self.data = data
        self.model = IsolationForest(contamination=0.1)

    def train_model(self):
        """Train the anomaly detection model."""
        self.model.fit(self.data)

    def detect_anomalies(self):
        """Detect anomalies in the data."""
        predictions = self.model.predict(self.data)
        anomalies = np.where(predictions == -1)[0]
        return anomalies

class BlockchainIdentity:
    """Class to manage identity on a mock blockchain."""
    def __init__(self):
        self.identities = {}

    def register_identity(self, user_id, data):
        """Register a new identity."""
        identity_hash = self.create_identity_hash(data)
        self.identities[user_id] = identity_hash
        print(f"Identity registered for {user_id}: {identity_hash}")

    def verify_identity(self, user_id, data):
        """Verify an identity using the hash."""
        identity_hash = self.create_identity_hash(data)
        if user_id in self.identities and self.identities[user_id] == identity_hash:
            print(f"Identity verified for {user_id}.")
            return True
        else:
            print(f"Identity verification failed for {user_id}.")
            return False

    def create_identity_hash(self, data):
        """Create a hash of the identity data."""
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

# Example usage
if __name__ == "__main__":
    # Sample KYC data (features could be age, income, etc.)
    kyc_data = np.array([[25, 50000], [30, 60000], [35, 70000], [40, 80000], [100, 1000000]])  # Last entry is an anomaly

    # Anomaly detection
    detector = AnomalyDetector(kyc_data)
    detector.train_model()
    anomalies = detector.detect_anomalies()
    print(f"Detected anomalies at indices: {anomalies}")

    # Blockchain identity management
    blockchain = BlockchainIdentity()
    user_id = "user123"
    user_data = {"name": "Alice", "age": 30, "income": 60000}

    # Register identity
    blockchain.register_identity(user_id, user_data)

    # Verify identity
    verification_result = blockchain.verify_identity(user_id, user_data)
