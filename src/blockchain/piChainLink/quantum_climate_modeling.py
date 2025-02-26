from qiskit import QuantumCircuit, Aer, execute
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class QuantumClimateModeling:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.backend = Aer.get_backend('statevector_simulator')

    def create_circuit(self, climate_data):
        """Create a quantum circuit for climate modeling."""
        qc = QuantumCircuit(self.num_qubits)

        # Normalize climate data to fit within the range of the quantum gates
        normalized_data = (climate_data - np.min(climate_data)) / (np.max(climate_data) - np.min(climate_data)) * np.pi

        # Encode climate data into the quantum circuit
        for i in range(len(normalized_data)):
            qc.ry(normalized_data[i], i % self.num_qubits)  # Rotate based on normalized climate data

        return qc

    def run(self, climate_data):
        """Run the quantum climate modeling circuit."""
        qc = self.create_circuit(climate_data)
        qc.measure_all()  # Measure all qubits
        job = execute(qc, self.backend, shots=1024)
        result = job.result()
        counts = result.get_counts()
        return counts

# Example usage
if __name__ == "__main__":
    # Generate synthetic climate data (e.g., temperature over time)
    time = np.linspace(0, 10, 100)
    climate_data = 20 + 5 * np.sin(time) + np.random.normal(0, 0.5, time.shape)  # Temperature data with noise

    # Initialize the quantum climate modeling
    num_qubits = min(len(climate_data), 5)  # Number of qubits based on the number of features
    climate_model = QuantumClimateModeling(num_qubits)

    # Run the quantum climate modeling
    counts = climate_model.run(climate_data)
    print(f"Model output counts: {counts}")

    # Plot the original climate data
    plt.plot(time, climate_data, label='Climate Data (Temperature)')
    plt.title('Synthetic Climate Data')
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    plt.legend()
    plt.show()
