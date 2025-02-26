import hashlib
import json
import numpy as np
import logging
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LogisticRegression
from cryptography.fernet import Fernet

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        logging.info(f"Customer identity registered for {customer_id}: {identity_hash}")

    def verify_identity(self, customer_id, data):
        """Verify a customer identity using the hash."""
        identity_hash = self.create_identity_hash(data)
        if customer_id in self.identities and self.identities[customer_id] == identity_hash:
            logging.info(f"Customer identity verified for {customer_id}.")
            return True
        else:
            logging.warning(f"Customer identity verification failed for {customer_id}.")
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

class TransactionHistory:
    """Class to manage transaction history for customers."""
    def __init__(self):
        self.history = {}

    def add_transaction(self, customer_id, transaction_info):
        """Add a transaction to the customer's history."""
        if customer_id not in self.history:
            self.history[customer_id] = []
        self.history[customer_id].append(transaction_info)

    def get_history(self, customer_id):
        """Get the transaction history for a customer."""
        return self.history.get(customer_id, [])

    def report_suspicious_activity(self, customer_id, transaction_info):
        """Report suspicious activity."""
        logging.warning(f"Suspicious activity reported for {customer_id}: {transaction_info}")

class PredictiveModel:
    """Class to predict the likelihood of a transaction being fraudulent."""
    def __init__(self):
        self.model = LogisticRegression()

    def train_model(self, X, y):
        """Train the predictive model."""
        self.model.fit(X, y)

    def predict(self, transaction):
        """Predict if a transaction is fraudulent."""
        return self.model.predict([transaction])

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
    # Sample transaction data for anomaly detection
    transaction_data = np.array([[500, 'Online', 'USA'], [15000, 'Cash', 'Canada'], 
                                  [200, 'Online', 'UK'], [25000, 'Cash', 'High Risk Country 1'], 
                                  [100, 'Online', 'Germany']])  # Last entry is an anomaly

    # Anomaly detection
    detector = AnomalyDetector(transaction_data[:, 0].astype(float).reshape(-1, 1))  # Only use the amount for anomaly detection
    detector.train_model()
    anomalies = detector.detect_anomalies()
    logging.info(f"Detected anomalies at indices: {anomalies}")

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
    logging.info(f"Risk level for transaction: {risk_level}")

    # Transaction history management
    transaction_history = TransactionHistory()
    transaction_history.add_transaction(customer_id, transaction_info)

    # Check transaction history
    history = transaction_history.get_history(customer_id)
    logging.info(f"Transaction history for {customer_id}: {history}")

    # Report suspicious activity
    if risk_level == "High":
        transaction_history.report_suspicious_activity(customer_id, transaction_info)

    # Predictive model usage
    predictive_model = PredictiveModel()
    # Sample training data (X: transaction features, y: labels indicating fraud)
    X_train = np.array([[500, 0], [15000, 1], [200, 0], [25000, 1], [100, 0]])  # Example features
    y_train = np.array([0, 1, 0, 1, 0])  # 0: Not Fraud, 1: Fraud
    predictive_model.train_model(X_train, y_train)

    # Predicting a new transaction
    new_transaction = [25000, 1]  # Example features for a new transaction
    prediction = predictive_model.predict(new_transaction)
    logging.info(f"Prediction for new transaction: {'Fraud' if prediction[0] == 1 else 'Not Fraud'}")

    # Data encryption example
    data_encryption = DataEncryption()
    encrypted_data = data_encryption.encrypt_data(customer_info)
    logging.info(f"Encrypted customer data: {encrypted_data}")

    decrypted_data = data_encryption.decrypt_data(encrypted_data)
    logging.info(f"Decrypted customer data: {decrypted_data}")
