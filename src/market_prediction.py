# src/market_prediction.py

import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib

class MarketPredictor:
    def __init__(self):
        self.model = RandomForestRegressor()

    def train(self, X, y):
        """Train the market prediction model."""
        self.model.fit(X, y)

    def predict(self, X):
        """Predict market prices."""
        return self.model.predict(X)

    def save_model(self, filename):
        """Save the trained model to a file."""
        joblib.dump(self.model, filename)

    def load_model(self, filename):
        """Load a trained model from a file."""
        self.model = joblib.load(filename)

# Example usage
if __name__ == "__main__":
    # Sample training data (features and labels)
    X = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
    y = np.array([1.5, 2.5, 3.5, 4.5])  # Example prices

    predictor = MarketPredictor()
    predictor.train(X, y)

    # Sample input for prediction
    X_test = np.array([[5, 6]])
    predictions = predictor.predict(X_test)
    print(f"Predicted price: {predictions}")
