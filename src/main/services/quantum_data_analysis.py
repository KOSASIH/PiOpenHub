# src/main/services/quantum_data_analysis.py

import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, Aer, execute
from qiskit.circuit.library import RealAmplitudes
from qiskit_machine_learning.algorithms import QSVC
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

class QuantumDataAnalysis:
    def __init__(self, n_qubits):
        self.n_qubits = n_qubits
        self.backend = Aer.get_backend('aer_simulator')
        self.model = QSVC(quantum_instance=self.backend)

    def preprocess_data(self, data):
        """Preprocess the data by scaling and reducing dimensions."""
        scaler = StandardScaler()
        data_normalized = scaler.fit_transform(data)

        # Use PCA for dimensionality reduction
        pca = PCA(n_components=self.n_qubits)
        data_reduced = pca.fit_transform(data_normalized)

        return data_reduced

    def train_model(self, X_train, y_train):
        """Train the quantum support vector classifier."""
        self.model.fit(X_train, y_train)

    def analyze_data(self, data, labels):
        """Analyze data using quantum algorithms."""
        # Preprocess the data
        data_reduced = self.preprocess_data(data)

        # Split the dataset
        X_train, X_test, y_train, y_test = train_test_split(data_reduced, labels, test_size=0.2, random_state=42)

        # Train the quantum model
        self.train_model(X_train, y_train)

        # Evaluate the model
        accuracy = self.model.score(X_test, y_test)
        print(f"Quantum Model Accuracy: {accuracy:.2f}")

        # Visualize the results
        self.visualize_results(X_test, y_test)

    def visualize_results(self, X_test, y_test):
        """Visualize the results of the quantum analysis."""
        plt.figure(figsize=(8, 6))
        plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap='viridis', edgecolor='k', s=50)
        plt.title('Quantum Data Analysis Results')
        plt.xlabel('Principal Component 1')
        plt.ylabel('Principal Component 2')
        plt.colorbar(label='Class Label')
        plt.grid()
        plt.show()

# Example usage
if __name__ == "__main__":
    # Load dataset
    iris = load_iris()
    data = iris.data
    labels = iris.target

    # Create an instance of the QuantumDataAnalysis class
    qda = QuantumDataAnalysis(n_qubits=2)

    # Analyze the data
    qda.analyze_data(data, labels)
