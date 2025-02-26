# quantum/quantumAlgorithms/quantum_algorithm_1.py

from qiskit import QuantumCircuit, Aer, execute

def run_quantum_algorithm_1():
    """Run a simple quantum algorithm to create a Bell state."""
    # Create a quantum circuit with 2 qubits
    circuit = QuantumCircuit(2)

    # Create a Bell state
    circuit.h(0)  # Apply Hadamard gate to the first qubit
    circuit.cx(0, 1)  # Apply CNOT gate (control: qubit 0, target: qubit 1)

    # Draw the circuit (optional)
    print("Quantum Circuit for Bell State:")
    print(circuit.draw())

    # Simulate the circuit
    simulator = Aer.get_backend('statevector_simulator')
    result = execute(circuit, simulator).result()
    statevector = result.get_statevector()

    print("Quantum Algorithm 1 Result (Statevector):", statevector)
    return statevector

# Example usage
if __name__ == "__main__":
    run_quantum_algorithm_1()
