# aiController.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from aiModel import AITask, AIDeployment
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize AI Task and Deployment
data_path = 'data.csv'  # Path to your dataset
ai_task = AITask(data_path)
ai_deployment = AIDeployment()

@app.route('/train', methods=['POST'])
def train_model():
    """Endpoint to train the AI model."""
    try:
        ai_task.load_data()
        X_train, X_test, y_train, y_test = ai_task.load_data()
        ai_task.build_model(input_shape=(X_train.shape[1],))
        ai_task.train_model(X_train, y_train)
        ai_task.save_model()
        return jsonify({"message": "Model trained successfully."}), 200
    except Exception as e:
        logger.error(f"Error training model: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint to make predictions using the trained model."""
    try:
        input_data = request.json.get('data')
        if input_data is None:
            return jsonify({"error": "No input data provided."}), 400
        
        input_data = np.array(input_data).reshape(1, -1)  # Reshape for a single sample
        ai_deployment.load_model()
        ai_deployment.load_scaler()
        predictions = ai_deployment.predict(input_data)
        return jsonify({"predictions": predictions.tolist()}), 200
    except Exception as e:
        logger.error(f"Error making predictions: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/evaluate', methods=['GET'])
def evaluate_model():
    """Endpoint to evaluate the AI model."""
    try:
        X_train, X_test, y_train, y_test = ai_task.load_data()
        ai_task.evaluate_model(X_test, y_test)
        return jsonify({"message": "Model evaluation completed."}), 200
    except Exception as e:
        logger.error(f"Error evaluating model: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/load_model', methods=['GET'])
def load_model():
    """Endpoint to load the trained model."""
    try:
        ai_deployment.load_model()
        return jsonify({"message": "Model loaded successfully."}), 200
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
