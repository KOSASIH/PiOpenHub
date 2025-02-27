# src/blockchain/piOpenChain/token_management.py

from web3 import Web3
import json

class TokenManagement:
    def __init__(self, provider_url, contract_address, abi):
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        self.contract = self.web3.eth.contract(address=contract_address, abi=abi)

    def mint_token(self, account, private_key, to_address, amount):
        """Mint new tokens to a specified address."""
        nonce = self.web3.eth.getTransactionCount(account)
        transaction = self.contract.functions.mint(to_address, amount).buildTransaction({
            'from': account,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': nonce
        })
        signed_txn = self.web3.eth.account.signTransaction(transaction, private_key)
        txn_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return self.web3.eth.waitForTransactionReceipt(txn_hash)

    def transfer_token(self, account, private_key, to_address, amount):
        """Transfer tokens from the caller's address to another address."""
        nonce = self.web3.eth.getTransactionCount(account)
        transaction = self.contract.functions.transfer(to_address, amount).buildTransaction({
            'from': account,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': nonce
        })
        signed_txn = self.web3.eth.account.signTransaction(transaction, private_key)
        txn_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return self.web3.eth.waitForTransactionReceipt(txn_hash)

    def get_balance(self, address):
        """Get the token balance of a specified address."""
        return self.contract.functions.balanceOf(address).call()

# Example usage
if __name__ == "__main__":
    provider_url = "https://mainnet.infura.io/v3/your_infura_project_id"
    contract_address = "0xYourTokenContractAddress"
    abi = json.loads('[{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"to","type":"address"},{"name":"amount","type":"uint256"}],"name":"mint","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"to","type":"address"},{"name":"amount","type":"uint256"}],"name":"transfer","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')

    token_manager = TokenManagement(provider_url, contract_address, abi)

    # Mint new tokens
    account = "0xYourEthereumAddress"
    private_key = "your_private_key"
    to_address = "0xRecipientAddress"
    amount = 1000  # Amount of tokens to mint
    receipt = token_manager.mint_token(account, private_key, to_address, amount)
    print(f"Tokens minted: {receipt}")

    # Transfer tokens
    transfer_amount = 500  # Amount of tokens to transfer
    transfer_receipt = token_manager.transfer_token(account, private_key, to_address, transfer_amount)
    print(f"Tokens transferred: {transfer_receipt}")

    # Get balance
    balance = token_manager.get_balance(to_address)
    print(f"Token balance of {to_address}: {balance}")
