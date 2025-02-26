import json
import hashlib

class SmartContract:
    def __init__(self, code):
        self.code = code  # The code of the smart contract
        self.state = {}  # State variables for the contract
        self.contract_id = self.calculate_contract_id()

    def calculate_contract_id(self):
        """Calculate a unique contract ID based on the contract code."""
        return hashlib.sha256(self.code.encode()).hexdigest()

    def execute(self, *args):
        """Execute the smart contract code with the provided arguments."""
        # For simplicity, we will use eval to execute the code.
        # In a real-world scenario, you would use a more secure method.
        try:
            exec(self.code, self.state, {'args': args})
            return self.state
        except Exception as e:
            print(f"Error executing contract: {e}")
            return None

    def get_state(self):
        """Return the current state of the smart contract."""
        return self.state

    def __repr__(self):
        return json.dumps({
            'contract_id': self.contract_id,
            'code': self.code,
            'state': self.state
        }, indent=4)

class SmartContractManager:
    def __init__(self):
        self.contracts = {}

    def deploy_contract(self, code):
        """Deploy a new smart contract and store it."""
        contract = SmartContract(code)
        self.contracts[contract.contract_id] = contract
        return contract.contract_id

    def execute_contract(self, contract_id, *args):
        """Execute a deployed smart contract."""
        contract = self.contracts.get(contract_id)
        if contract:
            return contract.execute(*args)
        else:
            print("Contract not found.")
            return None

    def get_contract_state(self, contract_id):
        """Get the state of a deployed smart contract."""
        contract = self.contracts.get(contract_id)
        if contract:
            return contract.get_state()
        else:
            print("Contract not found.")
            return None

# Example usage
if __name__ == "__main__":
    manager = SmartContractManager()

    # Define a simple smart contract code
    contract_code = """
def set_value(val):
    state['value'] = val

def get_value():
    return state.get('value', None)

# Example usage
set_value(args[0])
"""

    # Deploy the smart contract
    contract_id = manager.deploy_contract(contract_code)
    print(f"Contract deployed with ID: {contract_id}")

    # Execute the contract to set a value
    manager.execute_contract(contract_id, 42)

    # Retrieve the contract state
    state = manager.get_contract_state(contract_id)
    print("Contract State:", state)

    # Execute the contract to get the value
    value = manager.execute_contract(contract_id)
    print("Value from contract:", value)
