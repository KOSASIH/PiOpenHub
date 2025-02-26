# piSmartContracts/contract_interactor.py

import json
from web3 import Web3
from .config import Config

class ContractInteractor:
    def __init__(self, contract_address):
        # Initialize Web3 connection
        self.web3 = Web3(Web3.HTTPProvider(Config.INFURA_URL))
        if not self.web3.isConnected():
            raise Exception("Failed to connect to the Ethereum network.")
        
        # Load the contract instance
        self.contract = self.get_contract(contract_address)

    def get_contract(self, contract_address):
        """Get the contract instance."""
        with open(Config.CONTRACT_ABI) as f:
            abi = json.load(f)
        return self.web3.eth.contract(address=contract_address, abi=abi)

    def call_function(self, function_name, *args):
        """Call a read-only function of the smart contract."""
        try:
            result = getattr(self.contract.functions, function_name)(*args).call()
            return result
        except Exception as e:
            print(f"Error calling function '{function_name}': {e}")
            return None

    def send_transaction(self, function_name, *args):
        """Send a transaction to a state-changing function of the smart contract."""
        account = self.web3.eth.account.from_key(Config.PRIVATE_KEY)
        tx = getattr(self.contract.functions, function_name)(*args).buildTransaction({
            'from': account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(account.address),
        })
        
        # Sign the transaction
        signed_tx = self.web3.eth.account.signTransaction(tx, private_key=Config.PRIVATE_KEY)
        
        # Send the transaction
        try:
            tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            return tx_hash.hex()  # Return the transaction hash
        except Exception as e:
            print(f"Error sending transaction for function '{function_name}': {e}")
            return None

    def get_event_logs(self, event_name, from_block=0, to_block='latest'):
        """Get logs for a specific event emitted by the contract."""
        event_filter = self.contract.events[event_name].createFilter(fromBlock=from_block, toBlock=to_block)
        logs = event_filter.get_all_entries()
        return logs

# Example usage
if __name__ == "__main__":
    # Replace with your deployed contract address
    contract_address = Config.CONTRACT_ADDRESS

    # Initialize ContractInteractor
    interactor = ContractInteractor(contract_address)

    # Call a read-only function
    stored_value = interactor.call_function('get')
    print(f"Stored value: {stored_value}")

    # Send a transaction to change state
    tx_hash = interactor.send_transaction('set', 42)
    print(f"Transaction sent with hash: {tx_hash}")

    # Get event logs (replace 'YourEventName' with the actual event name)
    logs = interactor.get_event_logs('YourEventName')
    print(f"Event logs: {logs}")
