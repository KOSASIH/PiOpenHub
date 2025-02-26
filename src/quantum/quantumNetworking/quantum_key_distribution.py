# quantumNetworking/quantum_key_distribution.py

import random

def run_qkd(num_bits=10):
    """Run a simple quantum key distribution protocol (BB84)."""
    # Alice's random bit string
    alice_bits = [random.randint(0, 1) for _ in range(num_bits)]
    # Alice's random basis choice (0 for Z-basis, 1 for X-basis)
    alice_bases = [random.randint(0, 1) for _ in range(num_bits)]

    # Bob's random basis choice
    bob_bases = [random.randint(0, 1) for _ in range(num_bits)]

    # Key generation
    key = []
    for i in range(num_bits):
        if alice_bases[i] == bob_bases[i]:
            key.append(alice_bits[i])

    print("Alice's Bits:", alice_bits)
    print("Alice's Bases:", alice_bases)
    print("Bob's Bases:", bob_bases)
    print("Generated Key:", key)
    return key

# Example usage
if __name__ == "__main__":
    run_qkd()
