# src/quantum_ai/quantum_cryptography.py

import numpy as np
import random

class QuantumCryptography:
    def __init__(self, n_bits):
        self.n_bits = n_bits
        self.alice_bits = None
        self.alice_bases = None
        self.bob_bases = None
        self.shared_key = None

    def generate_bits_and_bases(self):
        """Alice generates random bits and random bases."""
        self.alice_bits = np.random.randint(0, 2, self.n_bits)
        self.alice_bases = np.random.randint(0, 2, self.n_bits)  # 0 for Z-basis, 1 for X-basis

    def send_bits(self):
        """Simulate sending bits from Alice to Bob."""
        bob_bases = np.random.randint(0, 2, self.n_bits)  # Bob chooses random bases
        self.bob_bases = bob_bases
        return bob_bases

    def measure_bits(self, bob_bases):
        """Bob measures the bits based on his chosen bases."""
        bob_measurements = []
        for i in range(self.n_bits):
            if bob_bases[i] == self.alice_bases[i]:  # If bases match, Bob measures correctly
                bob_measurements.append(self.alice_bits[i])
            else:  # If bases do not match, Bob gets a random bit
                bob_measurements.append(random.randint(0, 1))
        return bob_measurements

    def generate_shared_key(self, bob_measurements):
        """Generate the shared key based on matching bases."""
        key_indices = [i for i in range(self.n_bits) if self.alice_bases[i] == self.bob_bases[i]]
        self.shared_key = [self.alice_bits[i] for i in key_indices]
        return self.shared_key

# Example usage
if __name__ == "__main__":
    n_bits = 10  # Number of bits to send
    qc = QuantumCryptography(n_bits)

    # Step 1: Alice generates bits and bases
    qc.generate_bits_and_bases()
    print(f"Alice's bits: {qc.alice_bits}")
    print(f"Alice's bases: {qc.alice_bases}")

    # Step 2: Bob sends his bases
    bob_bases = qc.send_bits()
    print(f"Bob's bases: {bob_bases}")

    # Step 3: Bob measures the bits
    bob_measurements = qc.measure_bits(bob_bases)
    print(f"Bob's measurements: {bob_measurements}")

    # Step 4: Generate the shared key
    shared_key = qc.generate_shared_key(bob_measurements)
    print(f"Shared key: {shared_key}")
