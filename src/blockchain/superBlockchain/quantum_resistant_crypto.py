from ntru import NTRUEncrypt
import os
import base64

class QuantumResistantCrypto:
    def __init__(self):
        # Generate NTRU key pair
        self.ntru = NTRUEncrypt()
        self.private_key = self.ntru.generate_private_key()
        self.public_key = self.ntru.get_public_key()

    def encrypt(self, plaintext):
        """Encrypts the plaintext using the public key."""
        # Convert plaintext to bytes
        plaintext_bytes = plaintext.encode('utf-8')
        # Encrypt the plaintext
        ciphertext = self.ntru.encrypt(plaintext_bytes, self.public_key)
        # Return base64 encoded ciphertext for easy storage/transmission
        return base64.b64encode(ciphertext).decode('utf-8')

    def decrypt(self, ciphertext):
        """Decrypts the ciphertext using the private key."""
        # Decode the base64 encoded ciphertext
        ciphertext_bytes = base64.b64decode(ciphertext)
        # Decrypt the ciphertext
        decrypted_bytes = self.ntru.decrypt(ciphertext_bytes, self.private_key)
        # Convert bytes back to string
        return decrypted_bytes.decode('utf-8')

    def serialize_keys(self):
        """Serialize the public and private keys for storage."""
        public_key_serialized = self.ntru.serialize_public_key(self.public_key)
        private_key_serialized = self.ntru.serialize_private_key(self.private_key)
        return base64.b64encode(public_key_serialized).decode('utf-8'), base64.b64encode(private_key_serialized).decode('utf-8')

    def load_keys(self, public_key_b64, private_key_b64):
        """Load public and private keys from base64 encoded strings."""
        public_key_serialized = base64.b64decode(public_key_b64)
        private_key_serialized = base64.b64decode(private_key_b64)
        self.public_key = self.ntru.deserialize_public_key(public_key_serialized)
        self.private_key = self.ntru.deserialize_private_key(private_key_serialized)

# Example usage
if __name__ == "__main__":
    crypto = QuantumResistantCrypto()
    
    # Serialize keys
    public_key_b64, private_key_b64 = crypto.serialize_keys()
    print("Public Key (Base64):", public_key_b64)
    print("Private Key (Base64):", private_key_b64)

    # Encrypt a message
    message = "This is a secret message."
    encrypted_message = crypto.encrypt(message)
    print("Encrypted Message:", encrypted_message)

    # Decrypt the message
    decrypted_message = crypto.decrypt(encrypted_message)
    print("Decrypted Message:", decrypted_message)
