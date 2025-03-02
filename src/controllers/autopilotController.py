# autopilotController.py

from flask import Flask, request, jsonify
from autopilotService import AutopilotService
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Initialize the autopilot service
data_path = 'data.csv'  # Path to your dataset
autopilot_service = AutopilotService(data_path)

@app.route('/train', methods=['POST'])
def train_model():
    """Endpoint to train the autopilot model."""
    try:
        epochs = request.json.get('epochs', 100)  # Get epochs from request, default to 100
        autopilot_service.train_model(epochs=epochs)
        return jsonify({"message": "Model trained successfully."}), 200
    except Exception as e:
        logging.error(f"Error training model: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint to make predictions using the autopilot model."""
    try:
        new_data = request.json.get('data')  # Get new data from request
        if new_data is None:
            return jsonify({"error": "No data provided."}), 400
        predictions = autopilot_service.execute_autopilot(new_data)
        return jsonify({"predictions": predictions}), 200
    except Exception as e:
        logging.error(f"Error making predictions: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    """Endpoint to check the status of the autopilot service."""
    return jsonify({"status": "Autopilot service is running."}), 200

if __name__ == "__main__":
    app.run(debug=True)
