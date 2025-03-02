# collaborationService.py

import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class CollaborationService:
    def __init__(self):
        self.partners = []  # List to store partner information

    def add_partner(self, partner_info):
        """Add a new partner to the collaboration list."""
        self.partners.append(partner_info)
        logging.info(f"Partner added: {partner_info}")

    def remove_partner(self, partner_name):
        """Remove a partner from the collaboration list."""
        self.partners = [partner for partner in self.partners if partner['name'] != partner_name]
        logging.info(f"Partner removed: {partner_name}")

    def list_partners(self):
        """List all partners."""
        logging.info("Listing all partners:")
        for partner in self.partners:
            logging.info(partner)
        return self.partners

    def share_data_with_partner(self, partner_name, data):
        """Share data with a specific partner."""
        partner = next((p for p in self.partners if p['name'] == partner_name), None)
        if partner:
            try:
                response = requests.post(partner['api_endpoint'], json=data)
                if response.status_code == 200:
                    logging.info(f"Data shared successfully with {partner_name}.")
                    return response.json()
                else:
                    logging.error(f"Failed to share data with {partner_name}: {response.status_code} - {response.text}")
            except Exception as e:
                logging.error(f"Error sharing data with {partner_name}: {e}")
        else:
            logging.error(f"Partner {partner_name} not found.")

    def fetch_data_from_partner(self, partner_name):
        """Fetch data from a specific partner."""
        partner = next((p for p in self.partners if p['name'] == partner_name), None)
        if partner:
            try:
                response = requests.get(partner['api_endpoint'])
                if response.status_code == 200:
                    logging.info(f"Data fetched successfully from {partner_name}.")
                    return response.json()
                else:
                    logging.error(f"Failed to fetch data from {partner_name}: {response.status_code} - {response.text}")
            except Exception as e:
                logging.error(f"Error fetching data from {partner_name}: {e}")
        else:
            logging.error(f"Partner {partner_name} not found.")

# Example usage
if __name__ == "__main__":
    collaboration_service = CollaborationService()

    # Adding partners
    collaboration_service.add_partner({
        'name': 'IBM',
        'api_endpoint': 'https://api.ibm.com/data'
    })
    collaboration_service.add_partner({
        'name': 'Microsoft',
        'api_endpoint': 'https://api.microsoft.com/data'
    })

    # Listing partners
    collaboration_service.list_partners()

    # Sharing data with a partner
    data_to_share = {'key': 'value'}
    collaboration_service.share_data_with_partner('IBM', data_to_share)

    # Fetching data from a partner
    fetched_data = collaboration_service.fetch_data_from_partner('Microsoft')
    print(f"Fetched data: {fetched_data}")
