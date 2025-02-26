# ai/deployment/serve.py

from flask import Flask, request, jsonify
from .model_manager import ModelManager
from .config import Config

app = Flask(__name__)
model_manager = ModelManager()

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint to make predictions."""
    data = request.get_json()
    
    # Validate input data
    features = data.get('features')
    if not features or not isinstance(features, list):
        return jsonify({"error": "Invalid input. Please provide a list of features."}), 400
    
    try:
        # Make prediction
        prediction = model_manager.model.predict([features])
        return jsonify({"prediction": prediction.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def serve_model():
    """Serve the model using Flask."""
    model_manager.load_model()  # Load the model before serving
    app.run(host=Config.HOST, port=Config.PORT)

# Example usage
if __name__ == "__main__":
    serve_model()
