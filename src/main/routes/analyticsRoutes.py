# analyticsRoutes.py

from flask import Blueprint
from analyticsController import (
    load_data,
    preprocess_data,
    exploratory_data_analysis,
    train_model,
    visualize_predictions,
    save_model,
    load_model
)

# Create a Blueprint for analytics routes
analytics_routes = Blueprint('analytics_routes', __name__)

# Define the routes
analytics_routes.add_url_rule('/load_data', 'load_data', load_data, methods=['GET'])
analytics_routes.add_url_rule('/preprocess_data', 'preprocess_data', preprocess_data, methods=['POST'])
analytics_routes.add_url_rule('/eda', 'exploratory_data_analysis', exploratory_data_analysis, methods=['GET'])
analytics_routes.add_url_rule('/train_model', 'train_model', train_model, methods=['POST'])
analytics_routes.add_url_rule('/visualize_predictions', 'visualize_predictions', visualize_predictions, methods=['POST'])
analytics_routes.add_url_rule('/save_model', 'save_model', save_model, methods=['POST'])
analytics_routes.add_url_rule('/load_model', 'load_model', load_model, methods=['GET'])

# You can add more routes as needed
