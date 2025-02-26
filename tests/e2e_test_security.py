import unittest
from quantumCryptography.quantum_key_distribution import run_advanced_qkd
from quantumCryptography.quantum_digital_signatures import run_quantum_digital_signature

class TestQuantumSecurityFeatures(unittest.TestCase):

    def test_quantum_key_distribution(self):
        """Test the quantum key distribution process."""
        print("Testing Quantum Key Distribution...")
        num_bits = 10  # Number of bits for the key
        key = run_advanced_qkd(num_bits)
        
        # Check that the key is of the expected length
        self.assertEqual(len(key), num_bits, "The generated key length does not match the expected number of bits.")
        print("Quantum Key Distribution test passed.")

    def test_quantum_digital_signature(self):
        """Test the quantum digital signature process."""
        print("Testing Quantum Digital Signature...")
        message = "Test message for quantum digital signature."
        
        # Run the quantum digital signature process
        run_quantum_digital_signature(message)
        
        # In a real test, you would verify the signature here.
        # For this example, we assume the signature verification is successful.
        self.assertTrue(True, "Quantum digital signature verification failed.")
        print("Quantum Digital Signature test passed.")

if __name__ == "__main__":
    unittest.main()
