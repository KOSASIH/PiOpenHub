from qiskit import QuantumCircuit, Aer, execute

class QuantumFourierTransform:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.backend = Aer.get_backend('statevector_simulator')

    def create_circuit(self):
        """Create a quantum Fourier transform circuit."""
        qc = QuantumCircuit(self.num_qubits)

        for j in range(self.num_qubits):
            qc.h(j)  # Apply Hadamard gate

            for k in range(j + 1, self.num_qubits):
                qc.cp(np.pi / (2 ** (k - j)), k, j)  # Controlled phase rotation

        return qc

    def run(self):
        """Run the quantum Fourier transform circuit."""
        qc = self.create_circuit()
        job = execute(qc, self.backend)
        result = job.result()
        statevector = result.get_statevector()
        return statevector

# Example usage
if __name__ == "__main__":
    num_qubits = 3  # Number of qubits
    qft = QuantumFourierTransform(num_qubits)
    statevector = qft.run()
    print(f"Statevector after QFT: {statevector}")
