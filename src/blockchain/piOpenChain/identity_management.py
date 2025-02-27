# src/blockchain/piOpenChain/identity_management.py

from web3 import Web3
import json

class IdentityManagement:
    def __init__(self, provider_url, contract_address, abi):
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        self.contract = self.web3.eth.contract(address=contract_address, abi=abi)

    def create_identity(self, account, private_key, identity_data):
        """Create a new identity on the blockchain."""
        nonce = self.web3.eth.getTransactionCount(account)
        transaction = self.contract.functions.createIdentity(identity_data).buildTransaction({
            'from': account,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': nonce
        })
        signed_txn = self.web3.eth.account.signTransaction(transaction, private_key)
        txn_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return self.web3.eth.waitForTransactionReceipt(txn_hash)

    def get_identity(self, identity_id):
        """Retrieve identity information from the blockchain."""
        return self.contract.functions.getIdentity(identity_id).call()

# Example usage
if __name__ == "__main__":
    provider_url = "https://mainnet.infura.io/v3/your_infura_project_id"
    contract_address = "0xYourIdentityContractAddress"
    abi = json.loads('[{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"getIdentity","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"identityData","type":"string"}],"name":"createIdentity","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')

    identity_manager = IdentityManagement(provider_url, contract_address, abi)

    # Create a new identity
    account = "0xYourEthereumAddress"
    private_key = "your_private_key"
    identity_data = "User's identity data"
    receipt = identity_manager.create_identity(account, private_key, identity_data)
    print(f"Identity created: {receipt}")

    # Get identity information
    identity_id = 1  # Replace with a valid identity ID
    identity_info = identity_manager.get_identity(identity_id)
    print(f"Identity Info: {identity_info}")
