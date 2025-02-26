from qiskit import QuantumCircuit, Aer, execute

class QuantumKeyDistribution:
    def __init__(self):
        self.backend = Aer.get_backend('qasm_simulator')

    def create_circuit(self, basis_choice):
        """Create a QKD circuit based on the basis choice."""
        qc = QuantumCircuit(2, 1)  # 2 qubits, 1 classical bit

        # Prepare the qubit in a random state
        if basis_choice == 'Z':
            qc.h(0)  # Prepare in |+>
        else:
            qc.h(0)  # Prepare in |+>
            qc.t(0)  # Apply a T gate for |+>

        qc.measure(0, 0)  # Measure the first qubit
        return qc

    def run(self, basis_choice):
        """Run the QKD circuit."""
        qc = self.create_circuit(basis_choice)
        job = execute(qc, self.backend, shots=1)
        result = job.result()
        counts = result.get_counts()
        return counts

# Example usage
if __name__ == "__main__":
    qkd = QuantumKeyDistribution()
    basis_choice = 'Z'  # Example basis choice
    counts = qkd.run(basis_choice)
    print(f"Measurement results: {counts}")
