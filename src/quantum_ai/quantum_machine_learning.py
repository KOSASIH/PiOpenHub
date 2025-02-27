# src/quantum_ai/quantum_machine_learning.py

import time
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from qiskit import Aer
from qiskit.circuit.library import ZZFeatureMap, RealAmplitudes
from qiskit_machine_learning.algorithms.classifiers import VQC
from qiskit_machine_learning.optimizers import COBYLA

class QuantumMachineLearning:
    def __init__(self):
        self.backend = Aer.get_backend('aer_simulator')

    def load_data(self):
        """Load the Iris dataset."""
        iris_data = load_iris()
        features = iris_data.data
        labels = iris_data.target
        return features, labels

    def preprocess_data(self, features, labels):
        """Split the dataset into training and testing sets."""
        train_features, test_features, train_labels, test_labels = train_test_split(
            features, labels, train_size=0.8, random_state=123
        )
        return train_features, test_features, train_labels, test_labels

    def train_model(self, train_features, train_labels):
        """Train a Variational Quantum Classifier."""
        num_features = train_features.shape[1]
        feature_map = ZZFeatureMap(feature_dimension=num_features, reps=2)
        ansatz = RealAmplitudes(num_qubits=num_features, reps=3)
        optimizer = COBYLA(maxiter=100)

        vqc = VQC(
            feature_map=feature_map,
            ansatz=ansatz,
            optimizer=optimizer,
            sampler=self.backend
        )

        start = time.time()
        vqc.fit(train_features, train_labels)
        elapsed = time.time() - start
        print(f"Training time: {round(elapsed)} seconds")
        return vqc

    def evaluate_model(self, model, test_features, test_labels):
        """Evaluate the trained model."""
        predictions = model.predict(test_features)
        accuracy = accuracy_score(test_labels, predictions)
        print(f"Test Accuracy: {accuracy:.2f}")

# Example usage
if __name__ == "__main__":
    qml = QuantumMachineLearning()
    features, labels = qml.load_data()
    train_features, test_features, train_labels, test_labels = qml.preprocess_data(features, labels)
    model = qml.train_model(train_features, train_labels)
    qml.evaluate_model(model, test_features, test_labels)
