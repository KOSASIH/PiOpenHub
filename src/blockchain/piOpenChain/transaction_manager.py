# src/blockchain/piOpenChain/transaction_manager.py

from web3 import Web3

class TransactionManager:
    def __init__(self, provider_url):
        self.web3 = Web3(Web3.HTTPProvider(provider_url))

    def get_transaction(self, txn_hash):
        """Get transaction details by hash."""
        try:
            transaction = self.web3.eth.getTransaction(txn_hash)
            if transaction is None:
                raise ValueError("Transaction not found.")
            return transaction
        except Exception as e:
            print(f"Error retrieving transaction: {e}")
            return None

    def get_block(self, block_number):
        """Get block details by block number."""
        try:
            block = self.web3.eth.getBlock(block_number)
            if block is None:
                raise ValueError("Block not found.")
            return block
        except Exception as e:
            print(f"Error retrieving block: {e}")
            return None

    def get_latest_block(self):
        """Get the latest block."""
        try:
            latest_block = self.web3.eth.getBlock('latest')
            return latest_block
        except Exception as e:
            print(f"Error retrieving latest block: {e}")
            return None

# Example usage
if __name__ == "__main__":
    provider_url = "https://mainnet.infura.io/v3/your_infura_project_id"
    txn_manager = TransactionManager(provider_url)

    # Get the latest block
    latest_block = txn_manager.get_latest_block()
    print(f"Latest Block: {latest_block}")

    # Get a specific transaction
    txn_hash = "0xYourTransactionHash"
    transaction = txn_manager.get_transaction(txn_hash)
    print(f"Transaction Details: {transaction}")

    # Get a specific block
    block_number = 12345678  # Replace with a valid block number
    block = txn_manager.get_block(block_number)
    print(f"Block Details: {block}")
