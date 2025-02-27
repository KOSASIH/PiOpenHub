import numpy as np
from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram

class QuantumKeyDistribution:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.secret_key = []

    def prepare_states(self):
        """Prepare random quantum states for transmission."""
        states = []
        for _ in range(self.num_qubits):
            # Randomly choose between |0⟩, |1⟩, +, or - states
            if np.random.rand() < 0.5:
                states.append((0, 'Z'))  # |0⟩ or |1⟩ basis
            else:
                states.append((1, 'X'))  # + or - basis
        return states

    def measure_states(self, states):
        """Measure the quantum states."""
        measurements = []
        for state in states:
            qc = QuantumCircuit(1, 1)
            if state[1] == 'Z':
                qc.h(0)  # Prepare in the |+⟩ state for measurement in Z basis
            qc.measure(0, 0)

            # Simulate the circuit
            simulator = Aer.get_backend('qasm_simulator')
            result = execute(qc, backend=simulator, shots=1).result()
            measurement = list(result.get_counts(qc).keys())[0]
            measurements.append((measurement, state[1]))
        return measurements

    def generate_secret_key(self, measurements):
        """Generate a secret key based on measurements."""
        for measurement in measurements:
            if measurement[0] == '0' and measurement[1] == 'Z':
                self.secret_key.append(0)
            elif measurement[0] == '1' and measurement[1] == 'Z':
                self.secret_key.append(1)
            # Ignore measurements in the X basis for the key

    def run_qkd_protocol(self):
        """Run the BB84 QKD protocol."""
        print("Preparing quantum states...")
        states = self.prepare_states()
        print("Measuring quantum states...")
        measurements = self.measure_states(states)
        print("Generating secret key...")
        self.generate_secret_key(measurements)
        return self.secret_key

# Example usage
if __name__ == "__main__":
    num_qubits = 10  # Number of qubits to transmit
    qkd = QuantumKeyDistribution(num_qubits)
    secret_key = qkd.run_qkd_protocol()
    print("Generated Secret Key:", secret_key)
