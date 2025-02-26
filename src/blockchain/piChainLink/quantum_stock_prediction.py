from qiskit import QuantumCircuit, Aer, execute
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class QuantumStockPrediction:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.backend = Aer.get_backend('statevector_simulator')

    def create_circuit(self, stock_data):
        """Create a quantum circuit for stock prediction."""
        qc = QuantumCircuit(self.num_qubits)

        # Normalize stock data to fit within the range of the quantum gates
        normalized_data = (stock_data - np.min(stock_data)) / (np.max(stock_data) - np.min(stock_data)) * np.pi

        # Encode stock data into the quantum circuit
        for i in range(len(normalized_data)):
            qc.ry(normalized_data[i], i % self.num_qubits)  # Rotate based on normalized stock price

        return qc

    def run(self, stock_data):
        """Run the quantum stock prediction circuit."""
        qc = self.create_circuit(stock_data)
        qc.measure_all()  # Measure all qubits
        job = execute(qc, self.backend, shots=1024)
        result = job.result()
        counts = result.get_counts()
        return counts

# Example usage
if __name__ == "__main__":
    # Generate synthetic stock price data (e.g., a simple sine wave)
    time = np.linspace(0, 10, 100)
    stock_data = np.sin(time) + np.random.normal(0, 0.1, time.shape)  # Add some noise

    # Initialize the quantum stock prediction
    num_qubits = 5  # Number of qubits based on the number of features
    stock_predictor = QuantumStockPrediction(num_qubits)

    # Run the quantum stock prediction
    counts = stock_predictor.run(stock_data)
    print(f"Prediction counts: {counts}")

    # Plot the original stock data
    plt.plot(time, stock_data, label='Stock Price')
    plt.title('Synthetic Stock Price Data')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.show()
