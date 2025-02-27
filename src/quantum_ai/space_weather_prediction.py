import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import LSTM, Dense

class SpaceWeatherPredictor:
    def __init__(self):
        self.model = GradientBoostingRegressor()
        self.scaler = StandardScaler()

    def preprocess_data(self, data):
        """Preprocess the data for training."""
        # Normalize the features
        features = data.drop(columns=['target'])
        targets = data['target']
        features_scaled = self.scaler.fit_transform(features)
        return train_test_split(features_scaled, targets, test_size=0.2, random_state=42)

    def train_gradient_boosting(self, data):
        """Train a Gradient Boosting model."""
        X_train, X_test, y_train, y_test = self.preprocess_data(data)
        self.model.fit(X_train, y_train)
        predictions = self.model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        print("Gradient Boosting Model MSE:", mse)

    def train_lstm(self, data):
        """Train an LSTM model for time series prediction."""
        # Reshape data for LSTM
        data = data.values.reshape((data.shape[0], data.shape[1], 1))
        X_train, y_train = data[:-1], data[1:, -1]
        
        model = Sequential()
        model.add(LSTM(50, activation='relu', input_shape=(X_train.shape[1], 1)))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')
        
        model.fit(X_train, y_train, epochs=200, verbose=0)
        return model

    def predict_with_lstm(self, model, input_data):
        """Make predictions using the trained LSTM model."""
        input_data = input_data.reshape((1, input_data.shape[0], 1))
        return model.predict(input_data)

# Example usage
if __name__ == "__main__":
    # Simulated space weather data
    # Replace this with actual data loading
    data = pd.DataFrame({
        'feature1': np.random.rand(1000),
        'feature2': np.random.rand(1000),
        'target': np.random.rand(1000)
    })

    predictor = SpaceWeatherPredictor()
    
    # Train Gradient Boosting model
    predictor.train_gradient_boosting(data)

    # Train LSTM model
    lstm_model = predictor.train_lstm(data[['feature1', 'feature2', 'target']])

    # Example prediction with LSTM
    sample_input = np.array([data['feature1'].iloc[-1], data['feature2'].iloc[-1], data['target'].iloc[-1]])
    prediction = predictor.predict_with_lstm(lstm_model, sample_input)
    print("LSTM Prediction:", prediction)
