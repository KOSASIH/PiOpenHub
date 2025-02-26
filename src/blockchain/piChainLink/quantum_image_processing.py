from qiskit import QuantumCircuit, Aer, execute
import numpy as np
import matplotlib.pyplot as plt

class QuantumImageProcessing:
    def __init__(self, image):
        self.image = image
        self.backend = Aer.get_backend('statevector_simulator')

    def create_circuit(self):
        """Create a quantum circuit for image processing."""
        num_qubits = int(np.ceil(np.log2(self.image.size)))
        qc = QuantumCircuit(num_qubits)

        # Encode image data into the quantum circuit
        for i, pixel in enumerate(self.image.flatten()):
            qc.ry(pixel, i % num_qubits)  # Rotate based on pixel value

        return qc

    def run(self):
        """Run the quantum image processing circuit."""
        qc = self.create_circuit()
        qc.measure_all()  # Measure all qubits
        job = execute(qc, self.backend, shots=1024)
        result = job.result()
        statevector = result.get_statevector()
        return statevector

# Example usage
if __name__ == "__main__":
    # Create a simple grayscale image (10x10)
    image = np.random.rand(10, 10)  # Random pixel values

    # Initialize the quantum image processing
    image_processor = QuantumImageProcessing(image)

    # Run the image processing
    statevector = image_processor.run()
    print(f"Statevector after processing: {statevector}")

    # Display the original image
    plt.imshow(image, cmap='gray')
    plt.title('Original Image')
    plt.show()
