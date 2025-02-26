# piSmartContracts/contract_manager.py

import json
from web3 import Web3
from solcx import compile_source
from .config import Config

class ContractManager:
    def __init__(self):
        # Initialize Web3 connection
        self.web3 = Web3(Web3.HTTPProvider(Config.INFURA_URL))
        if not self.web3.isConnected():
            raise Exception("Failed to connect to the Ethereum network.")
        
        # Load account from private key
        self.account = self.web3.eth.account.from_key(Config.PRIVATE_KEY)

    def compile_contract(self, source_code):
        """Compile the smart contract source code."""
        compiled_sol = compile_source(source_code)
        contract_id, contract_interface = compiled_sol.popitem()
        return contract_id, contract_interface

    def deploy_contract(self, contract_interface, constructor_args=None):
        """Deploy the smart contract."""
        contract = self.web3.eth.contract(
            abi=contract_interface['abi'],
            bytecode=contract_interface['bin']
        )
        
        # Build transaction for contract deployment
        tx_hash = contract.constructor(*constructor_args).transact({
            'from': self.account.address,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei')
        })
        
        # Wait for transaction receipt
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        print(f"Contract deployed at address: {tx_receipt.contractAddress}")
        return tx_receipt.contractAddress

    def get_contract(self, contract_address):
        """Get the contract instance."""
        with open(Config.CONTRACT_ABI) as f:
            abi = json.load(f)
        return self.web3.eth.contract(address=contract_address, abi=abi)

    def get_account_balance(self):
        """Get the balance of the account."""
        balance = self.web3.eth.getBalance(self.account.address)
        return self.web3.fromWei(balance, 'ether')

    def estimate_gas(self, function_name, *args):
        """Estimate gas for a function call."""
        contract = self.get_contract(Config.CONTRACT_ADDRESS)
        gas_estimate = contract.functions[function_name](*args).estimateGas({
            'from': self.account.address
        })
        return gas_estimate

# Example usage
if __name__ == "__main__":
    # Example smart contract source code
    source_code = '''
    pragma solidity ^0.8.0;

    contract SimpleStorage {
        uint256 storedData;

        function set(uint256 x) public {
            storedData = x;
        }

        function get() public view returns (uint256) {
            return storedData;
        }
    }
    '''

    # Initialize ContractManager
    contract_manager = ContractManager()

    # Compile the contract
    contract_id, contract_interface = contract_manager.compile_contract(source_code)

    # Deploy the contract
    contract_address = contract_manager.deploy_contract(contract_interface)

    # Get account balance
    balance = contract_manager.get_account_balance()
    print(f"Account balance: {balance} ETH")

    # Estimate gas for a function call
    gas_estimate = contract_manager.estimate_gas('set', 42)
    print(f"Estimated gas for 'set' function: {gas_estimate}")
