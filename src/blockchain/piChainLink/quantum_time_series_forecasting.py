from qiskit import QuantumCircuit, Aer, execute
import numpy as np
import matplotlib.pyplot as plt

class QuantumTimeSeriesForecasting:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.backend = Aer.get_backend('statevector_simulator')

    def create_circuit(self, data):
        """Create a quantum circuit for time series forecasting."""
        qc = QuantumCircuit(self.num_qubits)

        # Normalize data to fit within the range of the quantum gates
        normalized_data = (data - np.min(data)) / (np.max(data) - np.min(data)) * np.pi

        # Encode time series data into the quantum circuit
        for i in range(len(normalized_data)):
            qc.ry(normalized_data[i], i % self.num_qubits)  # Rotate based on data value

        return qc

    def run(self, data):
        """Run the quantum time series forecasting circuit."""
        qc = self.create_circuit(data)
        qc.measure_all()  # Measure all qubits
        job = execute(qc, self.backend, shots=1024)
        result = job.result()
        counts = result.get_counts()
        return counts

    def forecast(self, data, steps=5):
        """Forecast future values based on the time series data."""
        # For simplicity, we will just return the last few values as a forecast
        # In a real implementation, you would use a more sophisticated approach
        forecasted_values = data[-steps:]  # Just returning the last values for demonstration
        return forecasted_values

# Example usage
if __name__ == "__main__":
    # Generate synthetic time series data (e.g., a sine wave)
    time = np.linspace(0, 10, 100)
    data = np.sin(time) + np.random.normal(0, 0.1, time.shape)  # Add some noise

    # Initialize the quantum time series forecasting
    num_qubits = 5  # Number of qubits based on the number of features
    forecasting = QuantumTimeSeriesForecasting(num_qubits)

    # Run the quantum forecasting
    counts = forecasting.run(data)
    print(f"Output counts: {counts}")

    # Forecast future values
    forecasted_values = forecasting.forecast(data, steps=5)
    print(f"Forecasted values: {forecasted_values}")

    # Plot the original data and forecasted values
    plt.plot(time, data, label='Original Data')
    plt.scatter(time[-5:], forecasted_values, color='red', label='Forecasted Values')
    plt.title('Quantum Time Series Forecasting')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.legend()
    plt.show()
