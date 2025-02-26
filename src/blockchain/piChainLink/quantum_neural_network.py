from qiskit import QuantumCircuit, Aer, execute
from qiskit.aer import AerSimulator
import numpy as np
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class QuantumNeuralNetwork:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.backend = AerSimulator()

    def create_circuit(self, params):
        """Create a quantum circuit for the neural network."""
        qc = QuantumCircuit(self.num_qubits)

        # Apply parameterized rotations
        for i in range(self.num_qubits):
            qc.rx(params[i], i)

        # Entanglement
        for i in range(self.num_qubits - 1):
            qc.cx(i, i + 1)

        return qc

    def run(self, params):
        """Run the quantum circuit and return the output."""
        qc = self.create_circuit(params)
        qc.measure_all()
        job = execute(qc, self.backend, shots=1024)
        result = job.result()
        counts = result.get_counts()
        return counts

# Example usage
if __name__ == "__main__":
    # Generate synthetic data
    X, y = make_moons(n_samples=100, noise=0.1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Initialize the quantum neural network
    qnn = QuantumNeuralNetwork(num_qubits=2)

    # Example parameters (random initialization)
    params = np.random.rand(2)

    # Run the quantum neural network
    counts = qnn.run(params)
    print(f"Output counts: {counts}")
