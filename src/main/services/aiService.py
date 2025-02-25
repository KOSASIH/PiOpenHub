import os
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import load_model

class AIService:
    def __init__(self, model_type='sklearn', model_path='model.h5'):
        self.model_type = model_type
        self.model_path = model_path
        self.model = None

    def load_data(self, file_path):
        """Load dataset from a CSV file."""
        return pd.read_csv(file_path)

    def preprocess_data(self, data, target_column):
        """Preprocess the data for training."""
        X = data.drop(columns=[target_column])
        y = data[target_column]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test

    def train_sklearn_model(self, X_train, y_train):
        """Train a scikit-learn model."""
        self.model = RandomForestClassifier()
        self.model.fit(X_train, y_train)

    def train_keras_model(self, X_train, y_train):
        """Train a TensorFlow Keras model."""
        model = keras.Sequential([
            layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
            layers.Dense(64, activation='relu'),
            layers.Dense(1, activation='sigmoid')  # Adjust for multi-class if needed
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        model.fit(X_train, y_train, epochs=10, batch_size=32)
        self.model = model

    def save_model(self):
        """Save the trained model to disk."""
        if self.model_type == 'sklearn':
            import joblib
            joblib.dump(self.model, 'sklearn_model.pkl')
        elif self.model_type == 'keras':
            self.model.save(self.model_path)

    def load_model(self):
        """Load a trained model from disk."""
        if self.model_type == 'sklearn':
            import joblib
            self.model = joblib.load('sklearn_model.pkl')
        elif self.model_type == 'keras':
            self.model = load_model(self.model_path)

    def predict(self, X):
        """Make predictions using the trained model."""
        if self.model is None:
            raise ValueError("Model is not trained or loaded.")
        return self.model.predict(X)

    def evaluate_model(self, X_test, y_test):
        """Evaluate the model's performance."""
        if self.model_type == 'sklearn':
            y_pred = self.model.predict(X_test)
            return accuracy_score(y_test, y_pred)
        elif self.model_type == 'keras':
            loss, accuracy = self.model.evaluate(X_test, y_test)
            return accuracy

# Example usage
if __name__ == "__main__":
    ai_service = AIService(model_type='keras')

    # Load and preprocess data
    data = ai_service.load_data('data.csv')
    X_train, X_test, y_train, y_test = ai_service.preprocess_data(data, target_column='target')

    # Train the model
    ai_service.train_keras_model(X_train, y_train)

    # Save the model
    ai_service.save_model()

    # Load the model
    ai_service.load_model()

    # Make predictions
    predictions = ai_service.predict(X_test)
    print("Predictions:", predictions)

    # Evaluate the model
    accuracy = ai_service.evaluate_model(X_test, y_test)
    print("Model Accuracy:", accuracy)
