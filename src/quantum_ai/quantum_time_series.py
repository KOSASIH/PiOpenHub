import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from qiskit import QuantumCircuit, Aer, execute

class QuantumTimeSeriesForecaster:
    def __init__(self):
        self.model = LinearRegression()
        self.scaler = StandardScaler()

    def prepare_data(self, time_series, n_steps):
        """Prepare the data for time series forecasting."""
        X, y = [], []
        for i in range(len(time_series) - n_steps):
            X.append(time_series[i:i + n_steps])
            y.append(time_series[i + n_steps])
        return np.array(X), np.array(y)

    def fit(self, time_series, n_steps):
        """Fit the linear regression model to the time series data."""
        X, y = self.prepare_data(time_series, n_steps)
        X_scaled = self.scaler.fit_transform(X)  # Scale features
        self.model.fit(X_scaled, y)

    def predict(self, input_data):
        """Make predictions using the fitted model."""
        input_scaled = self.scaler.transform(input_data)  # Scale input
        return self.model.predict(input_scaled)

    def quantum_transform(self, data):
        """Apply a quantum transformation to the data."""
        n = data.shape[0]
        qc = QuantumCircuit(n)
        qc.initialize(data.tolist(), range(n))
        qc.measure_all()

        # Simulate the circuit
        simulator = Aer.get_backend('qasm_simulator')
        result = execute(qc, backend=simulator, shots=1024).result()
        counts = result.get_counts(qc)

        transformed_data = np.zeros((len(counts), n))
        for i, (key, count) in enumerate(counts.items()):
            transformed_data[i] = [int(bit) for bit in key]
        return transformed_data

# Example usage
if __name__ == "__main__":
    # Simulated time series data (e.g., sine wave with noise)
    time_series = np.sin(np.linspace(0, 20, 100)) + np.random.normal(0, 0.1, 100)  # Sine wave with noise
    n_steps = 5  # Number of previous time steps to use for prediction

    forecaster = QuantumTimeSeriesForecaster()
    forecaster.fit(time_series, n_steps)

    # Prepare input for prediction
    input_data = time_series[-n_steps:].reshape(1, -1)  # Last n_steps for prediction
    prediction = forecaster.predict(input_data)
    print("Predicted next value:", prediction)

    # Apply quantum transformation
    transformed_data = forecaster.quantum_transform(time_series)
    print("Transformed Time Series Data:\n", transformed_data)
