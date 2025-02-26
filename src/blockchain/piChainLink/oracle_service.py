# piChainLink/oracle_service.py

from .chainlink_client import ChainlinkClient
from .data_processor import DataProcessor

class OracleService:
    def __init__(self):
        """Initialize the OracleService with a Chainlink client and data processor."""
        self.client = ChainlinkClient()
        self.data_processor = DataProcessor()

    def request_data(self, data):
        """Request data from the Chainlink oracle."""
        try:
            print("Sending request to Chainlink oracle...")
            request_response = self.client.create_request(data)
            print("Request sent successfully:", request_response)
            return request_response
        except Exception as e:
            print(f"Failed to request data: {e}")
            return None

    def process_response(self, request_id):
        """Process the response from the Chainlink oracle."""
        try:
            print(f"Fetching status for request ID: {request_id}...")
            status_response = self.client.get_request_status(request_id)
            print("Status response received:", status_response)

            # Process the data received from the oracle
            processed_data = self.data_processor.process(status_response)
            print("Processed data:", processed_data)
            return processed_data
        except Exception as e:
            print(f"Failed to process response: {e}")
            return None

    def send_transaction(self, transaction_data):
        """Send a transaction to the Ethereum network."""
        try:
            txn_hash = self.client.send_transaction(transaction_data)
            print(f"Transaction sent successfully. Hash: {txn_hash}")
            return txn_hash
        except Exception as e:
            print(f"Failed to send transaction: {e}")
            return None

    def listen_for_events(self, event_filter):
        """Listen for events from the Chainlink oracle."""
        try:
            print("Listening for events...")
            self.client.listen_for_events(event_filter)
        except Exception as e:
            print(f"Error listening for events: {e}")
