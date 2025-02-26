# piChainLink/chainlink_client.py

import requests
import json
from web3 import Web3
from .config import Config

class ChainlinkClient:
    def __init__(self):
        """Initialize the Chainlink client with configuration settings."""
        self.node_url = Config.CHAINLINK_NODE_URL
        self.oracle_address = Config.CHAINLINK_ORACLE_ADDRESS
        self.job_id = Config.CHAINLINK_JOB_ID
        self.private_key = Config.CHAINLINK_PRIVATE_KEY
        self.web3 = Web3(Web3.HTTPProvider(self.node_url))

    def create_request(self, data):
        """Create a request to the Chainlink oracle."""
        request_data = {
            "id": 1,
            "data": data,
            "jobId": self.job_id,
            "oracle": self.oracle_address,
            "privateKey": self.private_key
        }
        try:
            response = requests.post(f"{self.node_url}/v2/requests", json=request_data)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Error creating request: {e}")

    def get_request_status(self, request_id):
        """Get the status of a Chainlink request."""
        try:
            response = requests.get(f"{self.node_url}/v2/requests/{request_id}")
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Error fetching request status: {e}")

    def send_transaction(self, transaction_data):
        """Send a transaction to the Ethereum network."""
        try:
            # Prepare the transaction
            transaction = {
                'to': self.oracle_address,
                'value': self.web3.toWei(transaction_data['value'], 'ether'),
                'gas': transaction_data.get('gas', 2000000),
                'gasPrice': self.web3.toWei(transaction_data.get('gasPrice', '50'), 'gwei'),
                'nonce': self.web3.eth.getTransactionCount(transaction_data['from']),
                'data': transaction_data.get('data', b'')
            }

            # Sign the transaction
            signed_txn = self.web3.eth.account.signTransaction(transaction, self.private_key)

            # Send the transaction
            txn_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
            return self.web3.toHex(txn_hash)
        except Exception as e:
            raise Exception(f"Error sending transaction: {e}")

    def listen_for_events(self, event_filter):
        """Listen for events from the Chainlink oracle."""
        try:
            for event in event_filter.get_new_entries():
                print(f"New event: {event}")
        except Exception as e:
            raise Exception(f"Error listening for events: {e}")
