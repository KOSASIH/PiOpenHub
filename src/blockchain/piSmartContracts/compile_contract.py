# piSmartContracts/compile_contract.py

import os
from solcx import compile_source, install_solc
from solcx.exceptions import SolcError
from .config import Config

def compile_contract(contract_source):
    """Compile a Solidity contract and return its ABI and bytecode."""
    # Ensure the correct version of Solidity is installed
    install_solc('0.8.0')  # Specify the version you want to use

    try:
        # Compile the contract source code
        compiled_sol = compile_source(contract_source)
        
        # Extract the contract ID and interface
        contract_id, contract_interface = compiled_sol.popitem()
        print(f"Contract '{contract_id}' compiled successfully.")
        
        return contract_id, contract_interface
    except SolcError as e:
        print(f"Solidity compilation error: {e}")
        raise
    except Exception as e:
        print(f"An error occurred during compilation: {e}")
        raise

# Example usage
if __name__ == "__main__":
    # Example Solidity contract source code
    contract_source = """
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
    """

    try:
        contract_id, contract_interface = compile_contract(contract_source)
        print("Contract ID:", contract_id)
        print("Contract ABI:", contract_interface['abi'])
        print("Contract Bytecode:", contract_interface['bin'])
    except Exception as e:
        print(f"Failed to compile contract: {e}")
