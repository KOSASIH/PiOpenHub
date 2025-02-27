# src/main/services/market_prediction.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from qiskit import Aer
from qiskit_machine_learning.algorithms import VQC
from qiskit.circuit.library import RealAmplitudes

class MarketPrediction:
    def __init__(self, n_qubits):
        self.n_qubits = n_qubits
        self.classical_model = make_pipeline(StandardScaler(), LinearRegression())
        self.backend = Aer.get_backend('aer_simulator')
        self.quantum_model = None

    def prepare_data(self, data):
        """Prepare the data for training and testing."""
        # Feature engineering: Create lagged features for time series
        for lag in range(1, 4):  # Create 3 lagged features
            data[f'lag_{lag}'] = data['price'].shift(lag)
        data.dropna(inplace=True)

        X = data.drop(columns=['price'])
        y = data['price']
        return train_test_split(X, y, test_size=0.2, random_state=42)

    def train_classical_model(self, X_train, y_train):
        """Train the classical linear regression model."""
        self.classical_model.fit(X_train, y_train)

    def train_quantum_model(self, X_train, y_train):
        """Train a variational quantum classifier."""
        feature_map = RealAmplitudes(num_qubits=self.n_qubits, reps=2)
        ansatz = RealAmplitudes(num_qubits=self.n_qubits, reps=2)

        vqc = VQC(feature_map=feature_map, ansatz=ansatz, optimizer='SLSQP', backend=self.backend)
        vqc.fit(X_train.values, y_train.values)
        self.quantum_model = vqc

    def predict_classical(self, X_test):
        """Make predictions using the classical model."""
        return self.classical_model.predict(X_test)

    def predict_quantum(self, X_test):
        """Make predictions using the quantum model."""
        if self.quantum_model is None:
            raise ValueError("Quantum model has not been trained.")
        return self.quantum_model.predict(X_test.values)

    def evaluate_model(self, model, X_test, y_test):
        """Evaluate the model's performance."""
        predictions = model.predict(X_test)
        mse = np.mean((predictions - y_test) ** 2)
        return mse

    def visualize_predictions(self, y_test, classical_preds, quantum_preds):
        """Visualize the predictions of both models."""
        plt.figure(figsize=(12, 6))
        plt.plot(y_test.index, y_test, label='Actual Prices', color='black', linewidth=2)
        plt.plot(y_test.index, classical_preds, label='Classical Model Predictions', color='blue', linestyle='--')
        plt.plot(y_test.index, quantum_preds, label='Quantum Model Predictions', color='red', linestyle='--')
        plt.title('Market Price Predictions')
        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.legend()
        plt.show()

# Example usage
if __name__ == "__main__":
    # Generate synthetic time series data for market prediction
    np.random.seed(42)
    dates = pd.date_range(start='2020-01-01', periods=100)
    prices = np.random.normal(loc=100, scale=10, size=len(dates)).cumsum()
    data = pd.DataFrame({'date': dates, 'price': prices}).set_index('date')

    # Create an instance of the MarketPrediction class
    mp = MarketPrediction(n_qubits=4)

    # Prepare the data
    X_train, X_test, y_train, y_test = mp.prepare_data(data)

    # Train the classical model
    mp.train_classical_model(X_train, y_train)

    # Train the quantum model
    mp.train_quantum_model(X_train, y_train)

    # Make predictions
    classical_preds = mp.predict_classical(X_test)
    quantum_preds = mp.predict_quantum(X_test)

    # Evaluate models
    classical_mse = mp.evaluate_model(mp.classical_model, X_test, y_test)
    quantum_mse = mp.evaluate_model(mp.quantum_model, X_test, y_test)

    print(f"Classical Model MSE: {classical_mse:.2f}")
    print(f"Quantum Model MSE: {quantum_mse:.2f}")

    # Visualize predictions
    mp.visualize_predictions(y_test, classical_preds, quantum_preds)
