# src/quantum_ai/hybrid_quantum_classical.py

import numpy as np
from qiskit import QuantumCircuit, Aer, transpile, assemble, execute
from qiskit.circuit import Parameter
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.neural_network import MLPClassifier

class HybridQuantumClassical:
    def __init__(self, n_qubits):
        self.n_qubits = n_qubits
        self.backend = Aer.get_backend('aer_simulator')
        self.params = [Parameter(f'θ{i}') for i in range(n_qubits)]

    def quantum_circuit(self, params):
        """Create a quantum circuit for classification."""
        qc = QuantumCircuit(self.n_qubits)
        for i in range(self.n_qubits):
            qc.rx(params[i], i)  # Rotation around x-axis
        qc.measure_all()
        return qc

    def execute_circuit(self, params):
        """Execute the quantum circuit and return the results."""
        qc = self.quantum_circuit(params)
        transpiled_circuit = transpile(qc, self.backend)
        qobj = assemble(transpiled_circuit)
        result = execute(qobj, self.backend).result()
        counts = result.get_counts()
        return counts

    def classify(self, X_train, y_train, X_test):
        """Train a classical model using quantum features."""
        features = []
        for x in X_train:
            counts = self.execute_circuit(x)
            features.append(counts.get('0', 0))  # Count of '0' outcomes
        features = np.array(features).reshape(-1, 1)

        # Train a classical neural network
        clf = MLPClassifier(hidden_layer_sizes=(10,), max_iter=1000)
        clf.fit(features, y_train)

        # Generate features for test set
        test_features = []
        for x in X_test:
            counts = self.execute_circuit(x)
            test_features.append(counts.get('0', 0))
        test_features = np.array(test_features).reshape(-1, 1)

        return clf.predict(test_features)

# Example usage
if __name__ == "__main__":
    # Load dataset
    iris = load_iris()
    X = iris.data[:, :2]  # Use only the first two features for simplicity
    y = iris.target

    # One-hot encode labels
    encoder = OneHotEncoder(sparse=False)
    y_encoded = encoder.fit_transform(y.reshape(-1, 1))

    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

    # Create and train the hybrid model
    hybrid_model = HybridQuantumClassical(n_qubits=2)
    predictions = hybrid_model.classify(X_train, y_train.argmax(axis=1), X_test)

    print("Predictions:", predictions)
