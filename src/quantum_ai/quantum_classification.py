import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from qiskit import QuantumCircuit, Aer, execute
from qiskit.circuit.library import ZZFeatureMap
from qiskit_machine_learning.algorithms import QSVC
from qiskit.utils import QuantumInstance

class QuantumClassifier:
    def __init__(self):
        self.classical_model = SVC(kernel='linear')
        self.quantum_model = None

    def preprocess_data(self, data):
        """Preprocess the data for training."""
        features = data.drop(columns=['target'])
        targets = data['target']
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)
        return train_test_split(features_scaled, targets, test_size=0.2, random_state=42)

    def train_classical_model(self, data):
        """Train the classical SVM model."""
        X_train, X_test, y_train, y_test = self.preprocess_data(data)
        self.classical_model.fit(X_train, y_train)
        predictions = self.classical_model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print("Classical SVM Model Accuracy:", accuracy)

    def train_quantum_model(self, data):
        """Train the quantum SVM model."""
        X_train, X_test, y_train, y_test = self.preprocess_data(data)
        
        # Create a quantum feature map
        feature_map = ZZFeatureMap(feature_dimension=X_train.shape[1], reps=2)
        
        # Create a quantum instance
        quantum_instance = QuantumInstance(Aer.get_backend('aer_simulator'), shots=1024)
        
        # Create and train the quantum SVC model
        self.quantum_model = QSVC(feature_map=feature_map, quantum_instance=quantum_instance)
        self.quantum_model.fit(X_train, y_train)
        
        # Evaluate the quantum model
        predictions = self.quantum_model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print("Quantum SVC Model Accuracy:", accuracy)

# Example usage
if __name__ == "__main__":
    # Simulated dataset for classification
    data = pd.DataFrame({
        'feature1': np.random.rand(100),
        'feature2': np.random.rand(100),
        'target': np.random.choice([0, 1], size=100)
    })

    classifier = QuantumClassifier()
    
    # Train classical model
    classifier.train_classical_model(data)

    # Train quantum model
    classifier.train_quantum_model(data)
