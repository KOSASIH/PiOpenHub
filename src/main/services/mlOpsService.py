import os
import joblib
import mlflow
import mlflow.sklearn
from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class MLModelService:
    def __init__(self):
        # Set MLflow tracking URI
        mlflow.set_tracking_uri(os.getenv('MLFLOW_TRACKING_URI', 'http://localhost:5000'))
        self.model = None
        self.model_name = "IrisRandomForest"
        self.model_version = None

    def train_model(self):
        """Train a Random Forest model on the Iris dataset."""
        logging.info("Loading Iris dataset...")
        iris = load_iris()
        X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2, random_state=42)

        logging.info("Training Random Forest model...")
        self.model = RandomForestClassifier(n_estimators=100)
        self.model.fit(X_train, y_train)

        # Evaluate the model
        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        logging.info(f"Model accuracy: {accuracy:.2f}")

        # Log the model with MLflow
        with mlflow.start_run():
            mlflow.sklearn.log_model(self.model, self.model_name)
            mlflow.log_param("n_estimators", 100)
            mlflow.log_metric("accuracy", accuracy)

        # Get the model version
        self.model_version = mlflow.get_model_version(self.model_name, 1).version
        logging.info(f"Model trained and logged with version: {self.model_version}")

    def load_model(self):
        """Load the latest model version."""
        logging.info(f"Loading model version: {self.model_version}")
        self.model = mlflow.sklearn.load_model(f"models:/{self.model_name}/{self.model_version}")

    def predict(self, data):
        """Make predictions using the loaded model."""
        if self.model is None:
            logging.error("Model is not loaded. Please load the model before making predictions.")
            return None
        predictions = self.model.predict(data)
        return predictions.tolist()

# Initialize the ML model service
ml_service = MLModelService()

@app.route('/train', methods=['POST'])
def train():
    """Endpoint to train the model."""
    ml_service.train_model()
    return jsonify({"status": "success", "message": "Model trained successfully", "version": ml_service.model_version}), 200

@app.route('/load', methods=['GET'])
def load():
    """Endpoint to load the latest model."""
    ml_service.load_model()
    return jsonify({"status": "success", "message": "Model loaded successfully", "version": ml_service.model_version}), 200

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint to make predictions."""
    data = request.json.get('data')
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400

    predictions = ml_service.predict(data)
    if predictions is None:
        return jsonify({"status": "error", "message": "Model not loaded"}), 500

    return jsonify({"status": "success", "predictions": predictions}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
