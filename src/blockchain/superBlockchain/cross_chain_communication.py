import requests
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)

class CrossChainCommunication:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def send_transaction(self, transaction):
        """Send a transaction to the specified blockchain endpoint."""
        try:
            response = requests.post(self.endpoint, json=transaction)
            response.raise_for_status()  # Raise an error for bad responses
            logging.info(f"Transaction sent successfully: {transaction}")
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
            return {"error": str(http_err)}
        except requests.exceptions.ConnectionError as conn_err:
            logging.error(f"Connection error occurred: {conn_err}")
            return {"error": "Connection error"}
        except requests.exceptions.Timeout:
            logging.error("Request timed out")
            return {"error": "Request timed out"}
        except requests.exceptions.RequestException as req_err:
            logging.error(f"An error occurred: {req_err}")
            return {"error": str(req_err)}

    def get_transaction_status(self, transaction_id):
        """Get the status of a transaction by its ID."""
        try:
            response = requests.get(f"{self.endpoint}/transaction/{transaction_id}")
            response.raise_for_status()
            logging.info(f"Transaction status retrieved successfully for ID: {transaction_id}")
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
            return {"error": str(http_err)}
        except requests.exceptions.ConnectionError as conn_err:
            logging.error(f"Connection error occurred: {conn_err}")
            return {"error": "Connection error"}
        except requests.exceptions.Timeout:
            logging.error("Request timed out")
            return {"error": "Request timed out"}
        except requests.exceptions.RequestException as req_err:
            logging.error(f"An error occurred: {req_err}")
            return {"error": str(req_err)}

# Example usage
if __name__ == "__main__":
    # Configuration
    blockchain_endpoint = "https://other-blockchain.com/api/transaction"
    
    # Initialize the cross-chain communication client
    cross_chain = CrossChainCommunication(blockchain_endpoint)

    # Example transaction
    transaction = {
        "from": "address1",
        "to": "address2",
        "amount": 100,
        "currency": "ETH"
    }

    # Send a transaction
    response = cross_chain.send_transaction(transaction)
    print("Response from blockchain:", json.dumps(response, indent=4))

    # Example transaction status check
    transaction_id = "1234567890abcdef"
    status_response = cross_chain.get_transaction_status(transaction_id)
    print("Transaction status:", json.dumps(status_response, indent=4))
