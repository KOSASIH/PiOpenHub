# pi_crypto_connect.py

from web3 import Web3
from .exceptions import ConnectionError, TransactionError, InsufficientFundsError

class PiCryptoConnect:
    def __init__(self, provider_url, private_key):
        """Initialize the PiCryptoConnect instance."""
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        self.private_key = private_key
        self.account = self.web3.eth.account.from_key(private_key)

        if not self.web3.isConnected():
            raise ConnectionError("Failed to connect to the blockchain network.")

    def get_balance(self):
        """Get the balance of the connected account."""
        balance_wei = self.web3.eth.get_balance(self.account.address)
        balance_eth = self.web3.fromWei(balance_wei, 'ether')
        return balance_eth

    def create_transaction(self, to_address, amount_eth):
        """Create and sign a transaction."""
        amount_wei = self.web3.toWei(amount_eth, 'ether')
        nonce = self.web3.eth.getTransactionCount(self.account.address)

        transaction = {
            'to': to_address,
            'value': amount_wei,
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': nonce,
            'chainId': 1  # Mainnet ID; change as needed for testnets
        }

        # Check for sufficient funds
        if self.web3.eth.get_balance(self.account.address) < amount_wei:
            raise InsufficientFundsError("Insufficient funds for this transaction.")

        signed_txn = self.web3.eth.account.sign_transaction(transaction, self.private_key)
        txn_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return self.web3.toHex(txn_hash)

    def get_transaction_receipt(self, txn_hash):
        """Get the receipt of a transaction."""
        receipt = self.web3.eth.waitForTransactionReceipt(txn_hash)
        return receipt

# Example usage
if __name__ == "__main__":
    provider_url = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
    private_key = "YOUR_PRIVATE_KEY"

    try:
        crypto_connect = PiCryptoConnect(provider_url, private_key)
        print(f"Connected to blockchain. Balance: {crypto_connect.get_balance()} ETH")

        # Example transaction
        to_address = "0xRecipientAddressHere"
        amount = 0.01  # Amount in ETH
        txn_hash = crypto_connect.create_transaction(to_address, amount)
        print(f"Transaction sent! Hash: {txn_hash}")

        # Get transaction receipt
        receipt = crypto_connect.get_transaction_receipt(txn_hash)
        print(f"Transaction receipt: {receipt}")

    except ConnectionError as e:
        print(f"Connection error: {e}")
    except TransactionError as e:
        print(f"Transaction error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
