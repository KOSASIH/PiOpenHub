# collaborationController.py

from flask import Flask, request, jsonify
from collaborationService import CollaborationService
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Initialize the collaboration service
collaboration_service = CollaborationService()

@app.route('/partners', methods=['POST'])
def add_partner():
    """Endpoint to add a new partner."""
    try:
        partner_info = request.json
        collaboration_service.add_partner(partner_info)
        return jsonify({"message": "Partner added successfully."}), 201
    except Exception as e:
        logging.error(f"Error adding partner: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/partners/<string:partner_name>', methods=['DELETE'])
def remove_partner(partner_name):
    """Endpoint to remove a partner."""
    try:
        collaboration_service.remove_partner(partner_name)
        return jsonify({"message": "Partner removed successfully."}), 200
    except Exception as e:
        logging.error(f"Error removing partner: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/partners', methods=['GET'])
def list_partners():
    """Endpoint to list all partners."""
    try:
        partners = collaboration_service.list_partners()
        return jsonify(partners), 200
    except Exception as e:
        logging.error(f"Error listing partners: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/share/<string:partner_name>', methods=['POST'])
def share_data(partner_name):
    """Endpoint to share data with a specific partner."""
    try:
        data = request.json
        response = collaboration_service.share_data_with_partner(partner_name, data)
        return jsonify(response), 200
    except Exception as e:
        logging.error(f"Error sharing data with {partner_name}: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/fetch/<string:partner_name>', methods=['GET'])
def fetch_data(partner_name):
    """Endpoint to fetch data from a specific partner."""
    try:
        data = collaboration_service.fetch_data_from_partner(partner_name)
        return jsonify(data), 200
    except Exception as e:
        logging.error(f"Error fetching data from {partner_name}: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
