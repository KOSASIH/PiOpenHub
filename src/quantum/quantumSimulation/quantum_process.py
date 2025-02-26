# quantumSimulation/quantum_process.py

from qiskit import QuantumCircuit, Aer, execute

def simulate_quantum_process():
    """Simulate a simple quantum process (e.g., a Hadamard gate followed by a measurement)."""
    # Create a quantum circuit with 1 qubit and 1 classical bit
    circuit = QuantumCircuit(1, 1)

    # Apply a Hadamard gate to the qubit
    circuit.h(0)

    # Measure the qubit
    circuit.measure(0, 0)

    # Simulate the circuit using the QASM simulator
    simulator = Aer.get_backend('qasm_simulator')
    result = execute(circuit, simulator).result()
    
    # Get the counts of the measurement results
    counts = result.get_counts(circuit)

    print("Simulation Result (Counts):", counts)
    return counts

# Example usage
if __name__ == "__main__":
    simulate_quantum_process()
