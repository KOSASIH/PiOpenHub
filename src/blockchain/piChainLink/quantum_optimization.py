from qiskit import QuantumCircuit, Aer, execute
from qiskit.circuit import Parameter
import numpy as np

class QAOA:
    def __init__(self, num_qubits, p):
        self.num_qubits = num_qubits
        self.p = p
        self.backend = Aer.get_backend('statevector_simulator')

    def create_circuit(self, gamma, beta):
        """Create a QAOA circuit."""
        qc = QuantumCircuit(self.num_qubits)

        # Initialize the qubits to |+>
        qc.h(range(self.num_qubits))

        # Apply the QAOA layers
        for _ in range(self.p):
            # Apply the problem Hamiltonian (example: Max-Cut)
            for qubit in range(self.num_qubits):
                qc.rz(2 * gamma, qubit)  # Example rotation for the problem Hamiltonian

            # Apply the mixing Hamiltonian
            qc.rx(2 * beta, range(self.num_qubits))

        return qc

    def run(self, gamma, beta):
        """Run the QAOA circuit and return the statevector."""
        qc = self.create_circuit(gamma, beta)
        job = execute(qc, self.backend)
        result = job.result()
        statevector = result.get_statevector()
        return statevector

# Example usage
if __name__ == "__main__":
    num_qubits = 3  # Number of qubits
    p = 1  # Depth of the circuit
    qaoa = QAOA(num_qubits, p)

    # Example parameters
    gamma = np.pi / 4
    beta = np.pi / 4

    statevector = qaoa.run(gamma, beta)
    print(f"Statevector: {statevector}")
