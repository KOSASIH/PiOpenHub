# src/quantum_ai/quantum_image_processing.py

import numpy as np
from qiskit import QuantumCircuit, Aer, execute
import matplotlib.pyplot as plt

class QuantumImageProcessing:
    def __init__(self, image):
        self.image = image
        self.backend = Aer.get_backend('aer_simulator')

    def create_circuit(self):
        """Create a quantum circuit for image processing."""
        n = self.image.size  # Total number of pixels
        qc = QuantumCircuit(n)

        # Apply a Hadamard gate to each pixel (for demonstration)
        for i in range(n):
            if self.image.flatten()[i] == 1:  # If pixel is white (1), apply H gate
                qc.h(i)

        qc.measure_all()  # Measure all qubits
        return qc

    def process_image(self):
        """Process the image using a quantum circuit."""
        qc = self.create_circuit()
        job = execute(qc, self.backend, shots=1)
        result = job.result()
        counts = result.get_counts()

        # Convert counts to a binary string
        processed_image = list(counts.keys())[0]
        processed_image = np.array([int(bit) for bit in processed_image])

        # Reshape to original image dimensions
        return processed_image.reshape(self.image.shape)

    def display_image(self, image, title='Image'):
        """Display the image using Matplotlib."""
        plt.imshow(image, cmap='gray')
        plt.axis('off')
        plt.title(title)
        plt.show()

# Example usage
if __name__ == "__main__":
    # Create a simple binary image (for demonstration)
    image = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])  # 3x3 binary image
    qip = QuantumImageProcessing(image)

    # Display the original image
    qip.display_image(image, title='Original Image')

    # Process the image
    processed_image = qip.process_image()
    print("Processed Image:", processed_image)

    # Display the processed image
    qip.display_image(processed_image.reshape(image.shape), title='Processed Image')
