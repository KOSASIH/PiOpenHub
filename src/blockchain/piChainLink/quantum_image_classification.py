from qiskit import QuantumCircuit, Aer, execute
import numpy as np
from sklearn.datasets import load_sample_image
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

class QuantumImageClassification:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.backend = Aer.get_backend('statevector_simulator')

    def create_circuit(self, image_data):
        """Create a quantum circuit for image classification."""
        qc = QuantumCircuit(self.num_qubits)

        # Normalize image data
        normalized_data = MinMaxScaler().fit_transform(image_data.reshape(-1, 1)).flatten()

        # Encode image data into the quantum circuit
        for i in range(len(normalized_data)):
            qc.ry(normalized_data[i] * np.pi, i % self.num_qubits)  # Rotate based on pixel value

        return qc

    def run(self, image_data):
        """Run the quantum image classification circuit."""
        qc = self.create_circuit(image_data)
        qc.measure_all()  # Measure all qubits
        job = execute(qc, self.backend)
        result = job.result()
        statevector = result.get_statevector()
        return statevector

# Example usage
if __name__ == "__main__":
    # Load a sample image
    china = load_sample_image("china.jpg")
    image_data = china[:, :, 0].flatten()  # Use only one channel (grayscale)

    # Initialize the quantum image classification
    num_qubits = 8  # Number of qubits based on features
    classifier = QuantumImageClassification(num_qubits)

    # Run the quantum image classification
    statevector = classifier.run(image_data)
    print(f"Statevector after classification: {statevector}")

    # Display the original image
    plt.imshow(china)
    plt.title('Original Image')
    plt.axis('off')
    plt.show()
