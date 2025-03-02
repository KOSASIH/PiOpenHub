# analyticsRoutes.py

from flask import Blueprint, request, jsonify
from analyticsController import summary_statistics, correlation_matrix, histogram, generate_report

# Create a Blueprint for analytics routes
analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/summary', methods=['GET'])
def get_summary_statistics():
    """Route to get summary statistics of the dataset."""
    return summary_statistics()

@analytics_bp.route('/correlation', methods=['GET'])
def get_correlation_matrix():
    """Route to get the correlation matrix."""
    return correlation_matrix()

@analytics_bp.route('/histogram', methods=['POST'])
def create_histogram():
    """Route to generate a histogram for a specific column."""
    return histogram()

@analytics_bp.route('/report', methods=['GET'])
def get_report():
    """Route to generate a comprehensive report of the dataset."""
    return generate_report()

# Example of how to register the blueprint in your main application
# from flask import Flask
# app = Flask(__name__)
# app.register_blueprint(analytics_bp, url_prefix='/analytics')
