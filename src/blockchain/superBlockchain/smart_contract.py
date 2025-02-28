from web3 import Web3
from solcx import compile_source
import json

class SmartContract:
    def __init__(self, w3, contract_source):
        self.w3 = w3
        self.contract_source = contract_source
        self.contract = None
        self.contract_address = None

    def compile_contract(self):
        compiled_sol = compile_source(self.contract_source)
        contract_id, contract_interface = compiled_sol.popitem()
        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=contract_interface['abi']
        )
        return contract_interface

    def deploy_contract(self, account, gas_limit=3000000):
        compiled_contract = self.compile_contract()
        tx_hash = self.contract.constructor().transact({
            'from': account,
            'gas': gas_limit
        })
        self.w3.eth.waitForTransactionReceipt(tx_hash)
        self.contract_address = self.w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
        return self.contract_address

    def execute_function(self, function_name, *args, account=None):
        tx_hash = getattr(self.contract.functions, function_name)(*args).transact({'from': account})
        return self.w3.eth.waitForTransactionReceipt(tx_hash)

    def log_event(self, event_name):
        event_filter = self.contract.events[event_name].createFilter(fromBlock='latest')
        return event_filter.get_new_entries()

    def upgrade_contract(self, new_contract_source, account):
        new_compiled_contract = compile_source(new_contract_source)
        new_contract_id, new_contract_interface = new_compiled_contract.popitem()
        new_contract = self.w3.eth.contract(
            abi=new_contract_interface['abi']
        )
        tx_hash = new_contract.constructor().transact({'from': account})
        self.w3.eth.waitForTransactionReceipt(tx_hash)
        self.contract = new_contract
        return self.contract.address

# Example usage
if __name__ == "__main__":
    w3 = Web3(Web3.HTTPProvider('https://your.ethereum.node'))
    account = w3.eth.accounts[0]

    contract_source = '''
    pragma solidity ^0.8.0;

    contract SampleContract {
        string public data;

        event DataUpdated(string newData);

        function setData(string memory newData) public {
            data = newData;
            emit DataUpdated(newData);
        }
    }
    '''

    smart_contract = SmartContract(w3, contract_source)
    contract_address = smart_contract.deploy_contract(account)
    print("Contract deployed at:", contract_address)

    # Execute function
    smart_contract.execute_function('setData', 'Hello, Blockchain!', account)

    # Log events
    events = smart_contract.log_event('DataUpdated')
    print("New Events:", events)

    # Upgrade contract example
    new_contract_source = '''
    pragma solidity ^0.8.0;

    contract SampleContract {
        string public data;

        event DataUpdated(string newData);

        function setData(string memory newData) public {
            data = newData;
            emit DataUpdated(newData);
        }

        function getData() public view returns (string memory) {
            return data;
        }
    }
    '''
    upgraded_address = smart_contract.upgrade_contract(new_contract_source, account)
    print("Contract upgraded at:", upgraded_address)
