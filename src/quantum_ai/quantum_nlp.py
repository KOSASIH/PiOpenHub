# src/quantum_ai/quantum_nlp.py

import numpy as np
from qiskit import QuantumCircuit, Aer, execute
from qiskit.circuit.library import RealAmplitudes
from qiskit_machine_learning.algorithms import VQC
from qiskit_machine_learning.utils import split_dataset_to_data_and_labels
from sklearn.datasets import fetch_20newsgroups
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

class QuantumNLP:
    def __init__(self, n_qubits):
        self.n_qubits = n_qubits
        self.backend = Aer.get_backend('aer_simulator')
        self.vectorizer = TfidfVectorizer(max_features=10)  # Limit features for simplicity

    def encode_text(self, texts):
        """Encode text into TF-IDF representation."""
        return self.vectorizer.fit_transform(texts).toarray()

    def create_circuit(self, params):
        """Create a quantum circuit for classification."""
        qc = QuantumCircuit(self.n_qubits)
        for i in range(self.n_qubits):
            qc.ry(params[i], i)  # Apply rotation gates
        qc.measure_all()
        return qc

    def train_quantum_model(self, X_train, y_train):
        """Train a variational quantum classifier."""
        feature_map = RealAmplitudes(num_qubits=self.n_qubits, reps=2)
        ansatz = RealAmplitudes(num_qubits=self.n_qubits, reps=2)

        vqc = VQC(feature_map=feature_map, ansatz=ansatz, optimizer='SLSQP', backend=self.backend)
        vqc.fit(X_train, y_train)

        return vqc

    def predict(self, model, X_test):
        """Make predictions using the trained model."""
        predictions = []
        for x in X_test:
            # Create a circuit for each input
            qc = self.create_circuit(x)
            job = execute(qc, self.backend, shots=1024)
            result = job.result()
            counts = result.get_counts()
            prediction = max(counts, key=counts.get)  # Get the most frequent outcome
            predictions.append(prediction)
        return predictions

    def train_classical_model(self, X_train, y_train):
        """Train a classical model for comparison."""
        model = make_pipeline(TfidfVectorizer(), LogisticRegression())
        model.fit(X_train, y_train)
        return model

    def evaluate_model(self, model, X_test, y_test):
        """Evaluate the model's performance."""
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        return accuracy

# Example usage
if __name__ == "__main__":
    # Load dataset
    newsgroups = fetch_20newsgroups(subset='all', categories=['sci.space', 'comp.graphics'])
    X = newsgroups.data[:100]  # Use a subset for simplicity
    y = newsgroups.target[:100]

    # Encode labels
    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)

    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

    # Create and train the quantum NLP model
    n_qubits = 2  # Number of qubits
    quantum_nlp_model = QuantumNLP(n_qubits)

    # Encode training data
    X_train_encoded = quantum_nlp_model.encode_text(X_train)
    model = quantum_nlp_model.train_quantum_model(X_train_encoded, y_train)

    # Train a classical model for comparison
    classical_model = quantum_nlp_model.train_classical_model(X_train, y_train)

    # Evaluate both models
    quantum_accuracy = quantum_nlp_model.evaluate_model(model, X_test, y_test)
    classical_accuracy = quantum_nlp_model.evaluate_model(classical_model, X_test, y_test)

    print(f"Quantum Model Accuracy: {quantum_accuracy:.2f}")
    print(f"Classical Model Accuracy: {classical_accuracy:.2f}")
