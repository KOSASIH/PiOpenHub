import numpy as np

def basis_conversion(statevector):
    """Convert a statevector to probability distribution."""
    probabilities = np.abs(statevector) ** 2
    return probabilities

def print_probabilities(probabilities):
    """Print the probabilities in a readable format."""
    for i, prob in enumerate(probabilities):
        print(f"State |{i}>: Probability = {prob:.4f}")

# Example usage
if __name__ == "__main__":
    statevector = np.array([1/np.sqrt(2), 1/np.sqrt(2)])  # Example statevector
    probabilities = basis_conversion(statevector)
    print_probabilities(probabilities)
