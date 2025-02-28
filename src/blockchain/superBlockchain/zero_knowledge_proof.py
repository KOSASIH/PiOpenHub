import hashlib
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class ZeroKnowledgeProof:
    def __init__(self, secret):
        self.secret = secret
        self.nonce = os.urandom(16)  # Generate a random nonce

    def generate_proof(self):
        # Combine secret and nonce for proof generation
        combined = self.secret.encode() + self.nonce
        proof = hashlib.sha256(combined).hexdigest()
        logging.info(f"Generated proof: {proof} with nonce: {self.nonce.hex()}")
        return proof

    def verify_proof(self, proof):
        # Recreate the proof using the original secret and nonce
        combined = self.secret.encode() + self.nonce
        expected_proof = hashlib.sha256(combined).hexdigest()
        is_valid = proof == expected_proof
        logging.info(f"Verification result: {is_valid}")
        return is_valid

# Example usage
if __name__ == "__main__":
    secret = "my_secret"
    zkp = ZeroKnowledgeProof(secret)
    
    # Generate proof
    proof = zkp.generate_proof()
    
    # Verify proof
    is_valid = zkp.verify_proof(proof)
    print("Proof Valid:", is_valid)  # Output: True
