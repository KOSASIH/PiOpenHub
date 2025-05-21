# src/quantum_ai/quantum_ml.py

import numpy as np
from qiskit import QuantumCircuit, Aer, transpile
from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
from qiskit_machine_learning.algorithms import VQC
from qiskit_machine_learning.kernels import QuantumKernel
from qiskit.algorithms.optimizers import COBYLA, SPSA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

class QuantumML:
    """Quantum Machine Learning model using Qiskit."""
    
    def __init__(self, feature_dimension=2, num_qubits=None):
        """
        Initialize the Quantum ML model.
        
        Args:
            feature_dimension (int): Dimension of input features
            num_qubits (int, optional): Number of qubits to use. If None, uses feature_dimension.
        """
        self.feature_dimension = feature_dimension
        self.num_qubits = num_qubits if num_qubits is not None else feature_dimension
        self.backend = Aer.get_backend('aer_simulator')
        self.model = None
        self.scaler = StandardScaler()
        
    def _create_feature_map(self):
        """Create a feature map for encoding classical data into quantum states."""
        return ZZFeatureMap(feature_dimension=self.feature_dimension, reps=2)
        
    def _create_ansatz(self):
        """Create a variational ansatz for the model."""
        return RealAmplitudes(num_qubits=self.num_qubits, reps=2)
        
    def train(self, X, y, test_size=0.2, random_state=42):
        """
        Train the quantum ML model.
        
        Args:
            X (numpy.ndarray): Training features
            y (numpy.ndarray): Training labels
            test_size (float): Proportion of data to use for testing
            random_state (int): Random seed for reproducibility
            
        Returns:
            dict: Training results including accuracy and classification report
        """
        # Scale the features
        X_scaled = self.scaler.fit_transform(X)
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=test_size, random_state=random_state
        )
        
        # Create feature map and ansatz
        feature_map = self._create_feature_map()
        ansatz = self._create_ansatz()
        
        # Create the VQC model
        optimizer = SPSA(maxiter=100)
        self.model = VQC(
            feature_map=feature_map,
            ansatz=ansatz,
            optimizer=optimizer,
            callback=lambda x: None  # Empty callback to avoid verbose output
        )
        
        # Train the model
        self.model.fit(X_train, y_train)
        
        # Evaluate the model
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        
        return {
            'accuracy': accuracy,
            'classification_report': report,
            'X_test': X_test,
            'y_test': y_test,
            'y_pred': y_pred
        }
        
    def predict(self, X):
        """
        Make predictions using the trained model.
        
        Args:
            X (numpy.ndarray): Features to predict
            
        Returns:
            numpy.ndarray: Predicted labels
        """
        if self.model is None:
            raise ValueError("Model has not been trained yet.")
            
        # Scale the features
        X_scaled = self.scaler.transform(X)
        
        # Make predictions
        return self.model.predict(X_scaled)
        
    def create_quantum_kernel(self):
        """
        Create a quantum kernel for kernel-based machine learning.
        
        Returns:
            QuantumKernel: A quantum kernel instance
        """
        feature_map = self._create_feature_map()
        return QuantumKernel(feature_map=feature_map, quantum_instance=self.backend)

# Example usage
if __name__ == "__main__":
    # Generate some example data
    X = np.random.rand(20, 2)
    y = np.array([0, 1] * 10)
    
    # Create and train the model
    qml = QuantumML(feature_dimension=2)
    results = qml.train(X, y)
    
    print(f"Accuracy: {results['accuracy']}")
    print(f"Classification Report:\n{results['classification_report']}")
    
    # Make predictions on new data
    X_new = np.random.rand(5, 2)
    predictions = qml.predict(X_new)
    print(f"Predictions on new data: {predictions}")