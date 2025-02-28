import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from flask import Flask, request, jsonify
import joblib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class FraudDetectionModel:
    def __init__(self, model_path='fraud_model.pkl'):
        self.model_path = model_path
        self.model = None

    def load_model(self):
        """Load the trained model from a file."""
        self.model = joblib.load(self.model_path)
        logging.info("Model loaded successfully.")

    def predict(self, features):
        """Make a prediction based on input features."""
        if self.model is None:
            raise Exception("Model not loaded. Call load_model() first.")
        return self.model.predict(features)

def preprocess_data(data):
    """Preprocess the input data for model training."""
    # Handle missing values
    data.fillna(0, inplace=True)

    # Encode categorical variables if necessary
    # Example: data = pd.get_dummies(data, columns=['categorical_column'])

    # Normalize numerical features
    numerical_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    data[numerical_cols] = (data[numerical_cols] - data[numerical_cols].mean()) / data[numerical_cols].std()

    return data

def train_model(data):
    """Train the fraud detection model."""
    X = data.drop('Class', axis=1)  # Features
    y = data['Class']  # Target variable

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))

    # Save the model
    joblib.dump(model, 'fraud_model.pkl')
    logging.info("Model trained and saved successfully.")

# Flask application for real-time predictions
app = Flask(__name__)
fraud_model = FraudDetectionModel()

@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint for making predictions."""
    data = request.get_json(force=True)
    features = pd.DataFrame(data)
    prediction = fraud_model.predict(features)
    return jsonify({'prediction': prediction.tolist()})

if __name__ == "__main__":
    # Load the model
    fraud_model.load_model()

    # Example: Load and preprocess data, then train the model
    # df = pd.read_csv('path_to_your_data.csv')
    # df = preprocess_data(df)
    # train_model(df)

    # Start the Flask app
    app.run(host='0.0.0.0', port=5000)
