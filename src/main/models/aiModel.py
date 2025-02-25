# aiModel.py

import os
import logging
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIDeployment:
    def __init__(self, model_path='model.h5', scaler_path='scaler.pkl'):
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.model = None
        self.scaler = None

    def load_model(self):
        """Load the trained model from disk."""
        if os.path.exists(self.model_path):
            self.model = keras.models.load_model(self.model_path)
            logger.info("Model loaded successfully.")
        else:
            logger.error("Model file not found.")

    def load_scaler(self):
        """Load the scaler from disk."""
        if os.path.exists(self.scaler_path):
            self.scaler = joblib.load(self.scaler_path)
            logger.info("Scaler loaded successfully.")
        else:
            logger.error("Scaler file not found.")

    def predict(self, input_data):
        """Make predictions using the loaded model."""
        if self.model is None or self.scaler is None:
            logger.error("Model or scaler not loaded.")
            return None
        input_data_scaled = self.scaler.transform(input_data)
        predictions = self.model.predict(input_data_scaled)
        return np.argmax(predictions, axis=1)

class AITask:
    def __init__(self, data_path):
        self.data_path = data_path
        self.model = None
        self.scaler = StandardScaler()

    def load_data(self):
        """Load and preprocess the dataset."""
        logger.info("Loading data...")
        data = pd.read_csv(self.data_path)
        X = data.drop('target', axis=1)
        y = data['target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.scaler.fit(X_train)
        X_train_scaled = self.scaler.transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        logger.info("Data loaded and preprocessed.")
        return X_train_scaled, X_test_scaled, y_train, y_test

    def build_model(self, input_shape):
        """Build a neural network model."""
        logger.info("Building model...")
        model = keras.Sequential([
            layers.Input(shape=input_shape),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(32, activation='relu'),
            layers.Dense(1, activation='sigmoid')  # Change activation for multi-class
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        self.model = model
        logger.info("Model built successfully.")

    def train_model(self, X_train, y_train):
        """Train the model with early stopping and model checkpointing."""
        logger.info("Training model...")
        early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
        model_checkpoint = ModelCheckpoint('best_model.h5', save_best_only=True)

        self.model.fit(X_train, y_train, validation_split=0.2, epochs=50, batch_size=32,
                       callbacks=[early_stopping, model_checkpoint])
        logger.info("Model trained successfully.")

    def evaluate_model(self, X_test, y_test):
        """Evaluate the model on the test set."""
        logger.info("Evaluating model...")
        test_loss, test_accuracy = self.model.evaluate(X_test, y_test)
        logger.info(f"Test accuracy: {test_accuracy:.4f}")

        y_pred = (self.model.predict(X_test) > 0.5).astype("int32")
        print(classification_report(y_test, y_pred))
        print(confusion_matrix(y_test, y_pred))

    def save_model(self):
        """Save the trained model and scaler."""
        self.model.save('model.h5')
        joblib.dump(self.scaler, 'scaler.pkl')
        logger.info("Model and scaler saved successfully.")

if __name__ == "__main__":
    # Example usage
    data_path ```python
    = 'data.csv'  # Path to your dataset
    ai_task = AITask(data_path)
    X_train, X_test, y_train, y_test = ai_task.load_data()
    ai_task.build_model(input_shape=(X_train.shape[1],))
    ai_task.train_model(X_train, y_train)
    ai_task.evaluate_model(X_test, y_test)
    ai_task.save_model()

    # Deployment
    ai_deployment = AIDeployment()
    ai_deployment.load_model()
    ai_deployment.load_scaler()
    sample_input = np.array([[...], [...]])  # Replace with actual input data
    predictions = ai_deployment.predict(sample_input)
    print("Predictions:", predictions)
