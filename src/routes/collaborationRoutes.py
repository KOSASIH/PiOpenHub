# collaborationRoutes.py

from flask import Blueprint, request, jsonify
from collaborationController import add_partner, remove_partner, list_partners, share_data, fetch_data

# Create a Blueprint for collaboration routes
collaboration_bp = Blueprint('collaboration', __name__)

@collaboration_bp.route('/partners', methods=['POST'])
def add_new_partner():
    """Route to add a new partner."""
    return add_partner()

@collaboration_bp.route('/partners/<string:partner_name>', methods=['DELETE'])
def delete_partner(partner_name):
    """Route to remove a partner."""
    return remove_partner(partner_name)

@collaboration_bp.route('/partners', methods=['GET'])
def get_partners():
    """Route to list all partners."""
    return list_partners()

@collaboration_bp.route('/share/<string:partner_name>', methods=['POST'])
def share_data_with_partner(partner_name):
    """Route to share data with a specific partner."""
    return share_data(partner_name)

@collaboration_bp.route('/fetch/<string:partner_name>', methods=['GET'])
def fetch_data_from_partner(partner_name):
    """Route to fetch data from a specific partner."""
    return fetch_data(partner_name)

# Example of how to register the blueprint in your main application
# from flask import Flask
# app = Flask(__name__)
# app.register_blueprint(collaboration_bp, url_prefix='/collaboration')
