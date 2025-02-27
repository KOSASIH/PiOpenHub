# src/main/services/quantum_cryptography.py

import numpy as np
from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

class QuantumCryptography:
    def __init__(self):
        self.backend = Aer.get_backend('aer_simulator')

    def create_bb84_circuit(self, bits, bases):
        """Create a BB84 quantum key distribution circuit."""
        qc = QuantumCircuit(2, 1)  # 2 qubits, 1 classical bit

        # Prepare the qubit based on the chosen bit and basis
        for i in range(len(bits)):
            if bits[i] == '0':
                qc.h(0)  # Apply Hadamard to create superposition
            else:
                qc.x(0)  # Prepare |1> state

            if bases[i] == '1':
                qc.h(0)  # Change basis

            qc.measure(0, 0)  # Measure the qubit

        return qc

    def distribute_key(self, bits, bases):
        """Distribute a quantum key using BB84 protocol."""
        qc = self.create_bb84_circuit(bits, bases)
        job = execute(qc, self.backend, shots=1024)
        result = job.result()
        counts = result.get_counts()

        # Generate a key based on measurement results
        key = ''.join([bit for bit, count in counts.items() if count > 0])
        return key

    def visualize_distribution(self, counts):
        """Visualize the results of the key distribution."""
        plot_histogram(counts)
        plt.title("Measurement Results of Quantum Key Distribution")
        plt.show()

# Example usage
if __name__ == "__main__":
    # Example bits and bases for BB84 protocol
    bits = '10101010'  # Randomly chosen bits
    bases = '11001100'  # Randomly chosen bases

    qkc = QuantumCryptography()
    key = qkc.distribute_key(bits, bases)
    print("Distributed Quantum Key:", key)

    # Visualize the distribution results
    qc = qkc.create_bb84_circuit(bits, bases)
    job = execute(qc, qkc.backend, shots=1024)
    result = job.result()
    counts = result.get_counts()
    qkc.visualize_distribution(counts)
