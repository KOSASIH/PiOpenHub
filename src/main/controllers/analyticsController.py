# analyticsController.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from analyticsModel import AnalyticsModel
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize Analytics Model
data_path = 'data.csv'  # Path to your dataset
analytics_model = AnalyticsModel(data_path)

@app.route('/load_data', methods=['GET'])
def load_data():
    """Endpoint to load the dataset."""
    try:
        analytics_model.load_data()
        return jsonify({"message": "Data loaded successfully."}), 200
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/preprocess_data', methods=['POST'])
def preprocess_data():
    """Endpoint to preprocess the dataset."""
    try:
        analytics_model.preprocess_data()
        return jsonify({"message": "Data preprocessing completed."}), 200
    except Exception as e:
        logger.error(f"Error preprocessing data: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/eda', methods=['GET'])
def exploratory_data_analysis():
    """Endpoint to perform exploratory data analysis (EDA)."""
    try:
        analytics_model.exploratory_data_analysis()
        return jsonify({"message": "Exploratory data analysis completed."}), 200
    except Exception as e:
        logger.error(f"Error performing EDA: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/train_model', methods=['POST'])
def train_model():
    """Endpoint to train the analytics model."""
    target_column = request.json.get('target_column')
    if not target_column:
        return jsonify({"error": "Target column not provided."}), 400

    try:
        analytics_model.train_model(target_column)
        return jsonify({"message": "Model trained successfully."}), 200
    except Exception as e:
        logger.error(f"Error training model: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/visualize_predictions', methods=['POST'])
def visualize_predictions():
    """Endpoint to visualize model predictions."""
    try:
        X = analytics_model.data.drop('target', axis=1)  # Replace 'target' with your actual target column name
        y = analytics_model.data['target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        analytics_model.visualize_predictions(X_test, y_test)
        return jsonify({"message": "Predictions visualized successfully."}), 200
    except Exception as e:
        logger.error(f"Error visualizing predictions: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/save_model', methods=['POST'])
def save_model():
    """Endpoint to save the trained model."""
    try:
        analytics_model.save_model()
        return jsonify({"message": "Model saved successfully."}), 200
    except Exception as e:
        logger.error(f"Error saving model: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/load_model', methods=['GET'])
def load_model():
    """Endpoint to load the trained model."""
    try:
        analytics_model.load_model()
        return jsonify({"message": "Model loaded successfully."}), 200
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
