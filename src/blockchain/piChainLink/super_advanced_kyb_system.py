import hashlib
import json
import numpy as np
from sklearn.ensemble import IsolationForest

class AnomalyDetector:
    """Class to detect anomalies in business data."""
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
    """Class to manage business identity on a mock blockchain."""
    def __init__(self):
        self.identities = {}

    def register_identity(self, business_id, data):
        """Register a new business identity."""
        identity_hash = self.create_identity_hash(data)
        self.identities[business_id] = identity_hash
        print(f"Business identity registered for {business_id}: {identity_hash}")

    def verify_identity(self, business_id, data):
        """Verify a business identity using the hash."""
        identity_hash = self.create_identity_hash(data)
        if business_id in self.identities and self.identities[business_id] == identity_hash:
            print(f"Business identity verified for {business_id}.")
            return True
        else:
            print(f"Business identity verification failed for {business_id}.")
            return False

    def create_identity_hash(self, data):
        """Create a hash of the business identity data."""
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

class BusinessRiskAssessment:
    """Class to assess the risk level of a business."""
    def __init__(self, business_data):
        self.business_data = business_data

    def assess_risk(self):
        """Assess the risk level based on business data."""
        score = 0
        if self.business_data['revenue'] < 100000:
            score += 1  # Low revenue
        if self.business_data['years_in_business'] < 2:
            score += 1  # New business
        if self.business_data['industry'] in ['high-risk industry 1', 'high-risk industry 2']:
            score += 1  # High-risk industry

        risk_level = "Low" if score == 0 else "Medium" if score == 1 else "High"
        return risk_level

# Example usage
if __name__ == "__main__":
    # Sample business data for anomaly detection
    business_data = np.array([[50000, 1], [150000, 5], [200000, 10], [300000, 3], [10000, 1]])  # Last entry is an anomaly

    # Anomaly detection
    detector = AnomalyDetector(business_data)
    detector.train_model()
    anomalies = detector.detect_anomalies()
    print(f"Detected anomalies at indices: {anomalies}")

    # Blockchain identity management
    blockchain = BlockchainIdentity()
    business_id = "business123"
    business_info = {
        "name": "Tech Innovations LLC",
        "revenue": 150000,
        "years_in_business": 3,
        "industry": "Technology"
    }

    # Register business identity
    blockchain.register_identity(business_id, business_info)

    # Verify business identity
    verification_result = blockchain.verify_identity(business_id, business_info)

    # Risk assessment
    risk_assessment = BusinessRiskAssessment(business_info)
    risk_level = risk_assessment.assess_risk()
    print(f"Risk level for {business_info['name']}: {risk_level}")
