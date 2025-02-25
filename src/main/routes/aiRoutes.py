# aiRoutes.py

from flask import Blueprint
from aiController import train_model, predict, evaluate_model, load_model

# Create a Blueprint for AI routes
ai_routes = Blueprint('ai_routes', __name__)

# Define the routes
ai_routes.add_url_rule('/train', 'train_model', train_model, methods=['POST'])
ai_routes.add_url_rule('/predict', 'predict', predict, methods=['POST'])
ai_routes.add_url_rule('/evaluate', 'evaluate_model', evaluate_model, methods=['GET'])
ai_routes.add_url_rule('/load_model', 'load_model', load_model, methods=['GET'])

# You can add more routes as needed
