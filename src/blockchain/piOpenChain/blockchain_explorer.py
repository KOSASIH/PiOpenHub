# src/blockchain/piOpenChain/blockchain_explorer.py

from web3 import Web3

class BlockchainExplorer:
    def __init__(self, provider_url):
        self.web3 = Web3(Web3.HTTPProvider(provider_url))

    def get_transaction_history(self, address, start_block=0, end_block='latest'):
        """Retrieve transaction history for a given address."""
        transactions = []
        end_block = self.web3.eth.blockNumber if end_block == 'latest' else end_block

        for block_number in range(start_block, end_block + 1):
            block = self.web3.eth.getBlock(block_number, full_transactions=True)
            for txn in block.transactions:
                if txn['from'] == address or txn['to'] == address:
                    transactions.append(txn)

        return transactions

    def get_block_details(self, block_number):
        """Get detailed information about a specific block."""
        return self.web3.eth.getBlock(block_number, full_transactions=True)

# Example usage
if __name__ == "__main__":
    provider_url = "https://mainnet.infura.io/v3/your_infura_project_id"
    explorer = BlockchainExplorer(provider_url)

    # Get transaction history for a specific address
    address = "0xYourEthereumAddress"
    transactions = explorer.get_transaction_history(address)
    print(f"Transaction History for {address}: {transactions}")

    # Get details of a specific block
    block_number = 12345678  # Replace with a valid block number
    block_details = explorer.get_block_details(block_number)
    print(f"Block Details: {block_details}")
