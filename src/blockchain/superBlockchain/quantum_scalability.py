from qiskit import QuantumCircuit, Aer, transpile, assemble, execute
from qiskit.visualization import plot_histogram
import numpy as np

class QuantumScalability:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.circuit = QuantumCircuit(num_qubits)

    def apply_hadamard(self):
        """Apply Hadamard gates to all qubits."""
        for qubit in range(self.num_qubits):
            self.circuit.h(qubit)

    def apply_cnot(self, control, target):
        """Apply CNOT gate between control and target qubits."""
        self.circuit.cx(control, target)

    def apply_rotation(self, qubit, theta):
        """Apply a rotation gate to a specific qubit."""
        self.circuit.ry(theta, qubit)

    def optimize_circuit(self):
        """Optimize the quantum circuit for better performance."""
        self.circuit = transpile(self.circuit, optimization_level=3)

    def simulate(self):
        """Simulate the quantum circuit and return the results."""
        backend = Aer.get_backend('qasm_simulator')
        qobj = assemble(self.circuit)
        result = execute(self.circuit, backend, shots=1024).result()
        counts = result.get_counts(self.circuit)
        return counts

    def plot_results(self, counts):
        """Plot the results of the simulation."""
        plot_histogram(counts)

# Example usage
if __name__ == "__main__":
    num_qubits = 3
    quantum_scalability = QuantumScalability(num_qubits)

    # Apply gates
    quantum_scalability.apply_hadamard()
    quantum_scalability.apply_cnot(0, 1)
    quantum_scalability.apply_rotation(2, np.pi / 4)

    # Optimize the circuit
    quantum_scalability.optimize_circuit()

    # Simulate and plot results
    results = quantum_scalability.simulate()
    print("Simulation Results:", results)
    quantum_scalability.plot_results(results)
