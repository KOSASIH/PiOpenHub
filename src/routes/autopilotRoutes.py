# autopilotRoutes.py

from flask import Blueprint, request, jsonify
from autopilotController import train_model, predict, status

# Create a Blueprint for autopilot routes
autopilot_bp = Blueprint('autopilot', __name__)

@autopilot_bp.route('/train', methods=['POST'])
def train():
    """Route to train the autopilot model."""
    return train_model()

@autopilot_bp.route('/predict', methods=['POST'])
def make_prediction():
    """Route to make predictions using the autopilot model."""
    return predict()

@autopilot_bp.route('/status', methods=['GET'])
def check_status():
    """Route to check the status of the autopilot service."""
    return status()

# Example of how to register the blueprint in your main application
# from flask import Flask
# app = Flask(__name__)
# app.register_blueprint(autopilot_bp, url_prefix='/autopilot')
