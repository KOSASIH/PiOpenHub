import numpy as np
from quantum_key_distribution import QuantumKeyDistribution

class QuantumSecureCommunication:
    def __init__(self, num_qubits):
        self.qkd = QuantumKeyDistribution(num_qubits)
        self.secret_key = self.qkd.run_qkd_protocol()

    def encrypt_message(self, message):
        """Encrypt a message using the generated secret key."""
        # Convert message to binary
        binary_message = ''.join(format(ord(char), '08b') for char in message)
        # Ensure the secret key is long enough
        if len(binary_message) > len(self.secret_key):
            raise ValueError("Secret key is too short for the message length.")
        
        # Encrypt the message using XOR with the secret key
        encrypted_message = ''.join(str(int(bit) ^ self.secret_key[i]) for i, bit in enumerate(binary_message))
        return encrypted_message

    def decrypt_message(self, encrypted_message):
        """Decrypt a message using the generated secret key."""
        # Ensure the secret key is long enough
        if len(encrypted_message) > len(self.secret_key):
            raise ValueError("Secret key is too short for the encrypted message length.")
        
        # Decrypt the message using XOR with the secret key
        decrypted_message = ''.join(str(int(bit) ^ self.secret_key[i]) for i, bit in enumerate(encrypted_message))
        # Convert binary back to string
        chars = [chr(int(decrypted_message[i:i + 8], 2)) for i in range(0, len(decrypted_message), 8)]
        return ''.join(chars)

    def get_secret_key(self):
        """Return the generated secret key."""
        return self.secret_key

# Example usage
if __name__ == "__main__":
    num_qubits = 10
    secure_comm = QuantumSecureCommunication(num_qubits)

    original_message = "Hello, Quantum World!"
    print("Original Message:", original_message)

    # Encrypt the message
    encrypted_message = secure_comm.encrypt_message(original_message)
    print("Encrypted Message:", encrypted_message)

    # Decrypt the message
    decrypted_message = secure_comm.decrypt_message(encrypted_message)
    print("Decrypted Message:", decrypted_message)

    # Display the secret key
    print("Secret Key:", secure_comm.get_secret_key())
