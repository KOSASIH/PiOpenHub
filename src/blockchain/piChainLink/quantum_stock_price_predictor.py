from qiskit import QuantumCircuit, Aer, execute
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class QuantumStockPricePredictor:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.backend = Aer.get_backend('statevector_simulator')

    def create_circuit(self, stock_data):
        """Create a quantum circuit for stock price prediction."""
        qc = QuantumCircuit(self.num_qubits)

        # Normalize stock data
        normalized_data = (stock_data - np.min(stock_data)) / (np.max(stock_data) - np.min(stock_data)) * np.pi

        # Encode stock data into the quantum circuit
        for i in range(len(normalized_data)):
            qc.ry(normalized_data[i], i % self.num_qubits)

        return qc

    def run(self, stock_data):
        """Run the quantum stock price prediction circuit."""
        qc = self.create_circuit(stock_data)
        qc.measure_all()  # Measure all qubits
        job = execute(qc, self.backend)
        result = job.result()
        statevector = result.get_statevector()
        return statevector

# Example usage
if __name__ == "__main__":
    # Generate synthetic stock price data (e.g., a sine wave)
    time = np.linspace(0, 10, 100)
    stock_data = np.sin(time) + np.random.normal(0, 0.1, time.shape)  # Add some noise

    # Initialize the quantum stock price predictor
    num_qubits = 5  # Number of qubits based on features
    predictor = QuantumStockPricePredictor(num_qubits)

    # Run the quantum stock price prediction
    statevector = predictor.run(stock_data)
    print(f"Statevector after prediction: {statevector}")

    # Plot the original stock data
    plt.plot(time, stock_data, label='Stock Price')
    plt.title('Synthetic Stock Price Data')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.show()
