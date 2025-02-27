import numpy as np
from qiskit import QuantumCircuit, Aer, execute

class QuantumKeyDistribution:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.secret_key = []
        self.basis = []
        self.measurements = []

    def prepare_states(self):
        """Prepare random quantum states for transmission."""
        states = []
        for _ in range(self.num_qubits):
            if np.random.rand() < 0.5:
                states.append((0, 'Z'))  # |0⟩ or |1⟩ basis
                self.basis.append('Z')
            else:
                states.append((1, 'X'))  # + or - basis
                self.basis.append('X')
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
        for measurement, basis in measurements:
            if basis == 'Z':
                self.secret_key.append(int(measurement))
            # Discard measurements in the X basis

    def basis_reconciliation(self):
        """Perform basis reconciliation to ensure both parties have the same key."""
        # For simplicity, we assume Alice and Bob share their bases
        # In a real implementation, this would be done over a secure channel
        alice_bases = self.basis
        bob_bases = np.random.choice(['Z', 'X'], size=self.num_qubits)  # Simulated Bob's bases

        # Keep only the bits where bases match
        reconciled_key = [self.secret_key[i] for i in range(self.num_qubits) if alice_bases[i] == bob_bases[i]]
        return reconciled_key

    def run_qkd_protocol(self):
        """Run the BB84 QKD protocol."""
        states = self.prepare_states()
        measurements = self.measure_states(states)
        self.generate_secret_key(measurements)
        reconciled_key = self.basis_reconciliation()
        return reconciled_key

# Example usage
if __name__ == "__main__":
    num_qubits = 10
    qkd = QuantumKeyDistribution(num_qubits)
    secret_key = qkd.run_qkd_protocol()
    print("Generated Secret Key:", secret_key)
