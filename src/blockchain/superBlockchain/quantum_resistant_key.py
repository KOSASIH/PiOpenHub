import os
import ctypes
import numpy as np

# Load the shared library for OQS
libname = f"{os.getcwd()}/liboqs.so"  # Adjust the path as necessary
clib = ctypes.CDLL(libname)

# Define constants for key sizes
KYBER_PUBLIC_KEY_SIZE = 800  # Adjust based on the Kyber variant
KYBER_PRIVATE_KEY_SIZE = 1632  # Adjust based on the Kyber variant
KYBER_SHARED_SECRET_SIZE = 32  # Adjust based on the Kyber variant

def generate_quantum_resistant_key():
    """
    Generate a quantum-resistant key pair using the Kyber algorithm.
    """
    public_key = (ctypes.c_uint8 * KYBER_PUBLIC_KEY_SIZE)()
    private_key = (ctypes.c_uint8 * KYBER_PRIVATE_KEY_SIZE)()
    
    # Call the key generation function from the OQS library
    result = clib.kyber_keypair(public_key, private_key)
    
    if result != 0:
        raise Exception("Key generation failed")
    
    return bytes(public_key), bytes(private_key)

def save_key_to_file(key, filename):
    """
    Save the given key to a file in binary format.
    
    :param key: The key to save (public or private).
    :param filename: The filename to save the key to.
    """
    try:
        with open(filename, 'wb') as f:
            f.write(key)
        print(f"Key saved to {filename}")
    except IOError as e:
        print(f"Error saving key to file: {e}")

def load_key_from_file(filename):
    """
    Load a key from a file.
    
    :param filename: The filename to load the key from.
    :return: The loaded key.
    """
    try:
        with open(filename, 'rb') as f:
            return f.read()
    except IOError as e:
        print(f"Error loading key from file: {e}")
        return None

if __name__ == "__main__":
    # Generate the quantum-resistant key pair
    public_key, private_key = generate_quantum_resistant_key()

    # Save the keys to files
    save_key_to_file(public_key, "quantum_resistant_public_key.bin")
    save_key_to_file(private_key, "quantum_resistant_private_key.bin")

    print("Keys generated and saved successfully.")

    # Load the keys back from files
    loaded_public_key = load_key_from_file("quantum_resistant_public_key.bin")
    loaded_private_key = load_key_from_file("quantum_resistant_private_key.bin")

    print("Loaded Public Key:", loaded_public_key)
    print("Loaded Private Key:", loaded_private_key)
