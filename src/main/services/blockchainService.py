import requests
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BlockchainService:
    def __init__(self, node_url):
        self.node_url = node_url

    def get_block(self, block_number):
        """Retrieve a block by its number."""
        try:
            response = requests.get(f"{self.node_url}/blocks/{block_number}")
            response.raise_for_status()
            block_data = response.json()
            logging.info(f"Retrieved block {block_number}: {block_data}")
            return block_data
        except requests.exceptions.RequestException as e:
            logging.error(f"Error retrieving block {block_number}: {e}")
            return None

    def get_transaction(self, transaction_id):
        """Retrieve a transaction by its ID."""
        try:
            response = requests.get(f"{self.node_url}/transactions/{transaction_id}")
            response.raise_for_status()
            transaction_data = response.json()
            logging.info(f"Retrieved transaction {transaction_id}: {transaction_data}")
            return transaction_data
        except requests.exceptions.RequestException as e:
            logging.error(f"Error retrieving transaction {transaction_id}: {e}")
            return None

    def get_latest_block(self):
        """Retrieve the latest block in the blockchain."""
        try:
            response = requests.get(f"{self.node_url}/blocks/latest")
            response.raise_for_status()
            latest_block = response.json()
            logging.info(f"Retrieved latest block: {latest_block}")
            return latest_block
        except requests.exceptions.RequestException as e:
            logging.error(f"Error retrieving latest block: {e}")
            return None

    def send_transaction(self, transaction_data):
        """Send a transaction to the blockchain."""
        try:
            response = requests.post(f"{self.node_url}/transactions", json=transaction_data)
            response.raise_for_status()
            logging.info("Transaction sent successfully.")
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error sending transaction: {e}")
            return None

    def deploy_smart_contract(self, contract_data):
        """Deploy a smart contract to the blockchain."""
        try:
            response = requests.post(f"{self.node_url}/smart_contracts", json=contract_data)
            response.raise_for_status()
            logging.info("Smart contract deployed successfully.")
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error deploying smart contract: {e}")
            return None

    def call_smart_contract(self, contract_address, method_name, *args):
        """Call a method on a deployed smart contract."""
        try:
            payload = {
                "contract_address": contract_address,
                "method_name": method_name,
                "args": args
            }
            response = requests.post(f"{self.node_url}/smart_contracts/call", json=payload)
            response.raise_for_status()
            logging.info(f"Called smart contract method {method_name} successfully.")
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error calling smart contract method {method_name}: {e}")
            return None

# Example usage
if __name__ == "__main__":
    node_url = "https://api.blockchainnode.com"  # Example blockchain node URL
    blockchain_service = BlockchainService(node_url)

    # Retrieve the latest block
    latest_block = blockchain_service.get_latest_block()

    # Retrieve a specific block
    block_number = 5
    block_data = blockchain_service.get_block(block_number)

    # Retrieve a specific transaction
    transaction_id = "tx1234567890"
    transaction_data = blockchain_service.get_transaction(transaction_id)

    # Send a transaction
    transaction_payload = {
        "sender": "sender_address",
        "recipient": "recipient_address",
        "amount": 0.01
    }
    transaction_response = blockchain_service.send_transaction(transaction_payload)

    # Deploy a smart contract
    contract_payload = {
        "contract_name": "MySmartContract",
        "contract_code": "contract code here"
    }
    contract_response = blockchain_service.deploy_smart_contract(contract_payload)

    # Call a smart contract method
    contract_address = "0x1234567890abcdef"
    method_name = "myMethod"
    method_response = blockchain_service.call_smart_contract(contract_address, method_name, "arg1", "arg2")
