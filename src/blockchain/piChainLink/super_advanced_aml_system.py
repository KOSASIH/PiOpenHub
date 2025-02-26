import hashlib
import json
import numpy as np
from sklearn.ensemble import IsolationForest

class AnomalyDetector:
    """Class to detect anomalies in transaction data."""
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
    """Class to manage customer identity on a mock blockchain."""
    def __init__(self):
        self.identities = {}

    def register_identity(self, customer_id, data):
        """Register a new customer identity."""
        identity_hash = self.create_identity_hash(data)
        self.identities[customer_id] = identity_hash
        print(f"Customer identity registered for {customer_id}: {identity_hash}")

    def verify_identity(self, customer_id, data):
        """Verify a customer identity using the hash."""
        identity_hash = self.create_identity_hash(data)
        if customer_id in self.identities and self.identities[customer_id] == identity_hash:
            print(f"Customer identity verified for {customer_id}.")
            return True
        else:
            print(f"Customer identity verification failed for {customer_id}.")
            return False

    def create_identity_hash(self, data):
        """Create a hash of the customer identity data."""
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

class TransactionRiskAssessment:
    """Class to assess the risk level of a transaction."""
    def __init__(self, transaction_data):
        self.transaction_data = transaction_data

    def assess_risk(self):
        """Assess the risk level based on transaction data."""
        score = 0
        if self.transaction_data['amount'] > 10000:
            score += 1  # High transaction amount
        if self.transaction_data['country'] in ['High Risk Country 1', 'High Risk Country 2']:
            score += 1  # High-risk country
        if self.transaction_data['transaction_type'] == 'cash':
            score += 1  # Cash transactions are riskier

        risk_level = "Low" if score == 0 else "Medium" if score == 1 else "High"
        return risk_level

# Example usage
if __name__ == "__main__":
    # Sample transaction data for anomaly detection
    transaction_data = np.array([[500, 'Online', 'USA'], [15000, 'Cash', 'Canada'], 
                                  [200, 'Online', 'UK'], [25000, 'Cash', 'High Risk Country 1'], 
                                  [100, 'Online', 'Germany']])  # Last entry is an anomaly

    # Anomaly detection
    detector = AnomalyDetector(transaction_data[:, 0].astype(float).reshape(-1, 1))  # Only use the amount for anomaly detection
    detector.train_model()
    anomalies = detector.detect_anomalies()
    print(f"Detected anomalies at indices: {anomalies}")

    # Blockchain identity management
    blockchain = BlockchainIdentity()
    customer_id = "customer123"
    customer_info = {
        "name": "John Doe",
        "age": 35,
        "country": "USA"
    }

    # Register customer identity
    blockchain.register_identity(customer_id, customer_info)

    # Verify customer identity
    verification_result = blockchain.verify_identity(customer_id, customer_info)

    # Transaction risk assessment
    transaction_info = {
        "amount": 25000,
        "country": "High Risk Country 1",
        "transaction_type": "Cash"
    }
    risk_assessment = TransactionRiskAssessment(transaction_info)
    risk_level = risk_assessment.assess_risk()
    print(f"Risk level for transaction: {risk_level}")
