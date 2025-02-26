from qiskit import QuantumCircuit, Aer, execute
import numpy as np
from sklearn.datasets import load_iris
from sklearn.feature_selection import SelectKBest, f_classif

class QuantumFeatureSelection:
    def __init__(self, num_features):
        self.num_features = num_features
        self.backend = Aer.get_backend('statevector_simulator')

    def create_circuit(self, features):
        """Create a quantum circuit for feature selection."""
        qc = QuantumCircuit(self.num_features)

        # Example: Prepare the circuit based on feature values
        for i in range(self.num_features):
            qc.ry(features[i], i)  # Rotate based on feature value

        return qc

    def run(self, features):
        """Run the quantum feature selection circuit."""
        qc = self.create_circuit(features)
        job = execute(qc, self.backend)
        result = job.result()
        statevector = result.get_statevector()
        return statevector

# Example usage
if __name__ == "__main__":
    # Load dataset
    iris = load_iris()
    X = iris.data
    y = iris.target

    # Select best features using classical method
    selector = SelectKBest(score_func=f_classif, k=2)
    X_new = selector.fit_transform(X, y)

    # Initialize quantum feature selection
    num_features = X_new.shape[1]
    qfs = QuantumFeatureSelection(num_features)

    # Run the quantum feature selection
    for features in X_new:
        statevector = qfs.run(features)
        print(f"Statevector for features {features}: {statevector}")
