from qiskit import QuantumCircuit, Aer, execute
import numpy as np
import random

class Alice:
    def __init__(self, num_bits):
        self.num_bits = num_bits
        self.bits = np.random.randint(0, 2, num_bits)  # Random bits (0 or 1)
        self.bases = np.random.randint(0, 2, num_bits)  # Random bases (0 or 1)

    def encode(self):
        """Encode bits into qubits based on random bases."""
        circuits = []
        for i in range(self.num_bits):
            qc = QuantumCircuit(1, 1)
            if self.bases[i] == 0:  # Z-basis
                if self.bits[i] == 1:
                    qc.x(0)  # Apply X gate to encode '1'
            else:  # X-basis
                if self.bits[i] == 1:
                    qc.h(0)  # Apply H gate to encode '1'
            circuits.append(qc)
        return circuits

class Bob:
    def __init__(self, num_bits):
        self.num_bits = num_bits
        self.bases = np.random.randint(0, 2, num_bits)  # Random bases (0 or 1)

    def measure(self, circuits):
        """Measure the qubits based on random bases."""
        results = []
        for i in range(self.num_bits):
            qc = circuits[i]
            if self.bases[i] == 1:  # Measure in X-basis
                qc.h(0)  # Apply H gate before measurement
            qc.measure(0, 0)  # Measure the qubit
            job = execute(qc, Aer.get_backend('qasm_simulator'), shots=1)
            result = job.result().get_counts()
            measured_bit = int(list(result.keys())[0])  # Get the measured bit
            results.append(measured_bit)
        return results

def sift_keys(alice, bob):
    """Sift the keys by comparing bases."""
    key_a = []
    key_b = []
    for i in range(alice.num_bits):
        if alice.bases[i] == bob.bases[i]:  # Bases match
            key_a.append(alice.bits[i])
            key_b.append(bob.measure(circuits)[i])  # Use Bob's measured bit
    return key_a, key_b

def check_for_eavesdropping(key_a, key_b):
    """Check for eavesdropping by comparing a subset of the keys."""
    num_to_check = min(len(key_a), 10)  # Check the first 10 bits
    errors = sum(1 for i in range(num_to_check) if key_a[i] != key_b[i])
    error_rate = errors / num_to_check
    return error_rate

# Example usage
if __name__ == "__main__":
    num_bits = 20  # Number of bits to send
    alice = Alice(num_bits)
    circuits = alice.encode()  # Alice encodes her bits into qubits

    bob = Bob(num_bits)
    measured_bits = bob.measure(circuits)  # Bob measures the qubits

    # Sift the keys
    key_a, key_b = sift_keys(alice, bob)

    # Check for eavesdropping
    error_rate = check_for_eavesdropping(key_a, key_b)
    print(f"Alice's key: {key_a}")
    print(f"Bob's key: {key_b}")
    print(f"Error rate: {error_rate:.2%}")

    if error_rate > 0:
        print("Eavesdropping detected!")
    else:
        print("No eavesdropping detected.")
