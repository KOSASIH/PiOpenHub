# pi_stellar_nexus.py

from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset
from .exceptions import ConnectionError, TransactionError, InsufficientFundsError

class PiStellarNexus:
    def __init__(self, horizon_url, secret_key):
        """Initialize the PiStellarNexus instance."""
        self.server = Server(horizon_url)
        self.keypair = Keypair.from_secret(secret_key)

        # Check if the account exists
        try:
            self.server.accounts().account_id(self.keypair.public_key).call()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to the Stellar network: {e}")

    def get_balance(self):
        """Get the balance of the connected account."""
        account = self.server.accounts().account_id(self.keypair.public_key).call()
        balances = account['balances']
        return {balance['asset_type']: balance['balance'] for balance in balances}

    def create_transaction(self, to_address, amount, asset_code='XLM'):
        """Create and sign a transaction."""
        # Check for sufficient funds
        balance = self.get_balance().get('native', 0)
        if balance < amount:
            raise InsufficientFundsError("Insufficient funds for this transaction.")

        # Create the transaction
        transaction = (
            TransactionBuilder(
                source_account=self.server.load_account(self.keypair.public_key),
                network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,  # Change to MAINNET_NETWORK_PASSPHRASE for mainnet
                base_fee=100,
            )
            .add_text_memo("Transaction from PiStellarNexus")
            .add_operation(
                operation=Payment(
                    destination=to_address,
                    asset=Asset.native(),
                    amount=str(amount),
                )
            )
            .build()
        )

        # Sign the transaction
        transaction.sign(self.keypair)
        try:
            response = self.server.submit_transaction(transaction)
            return response
        except Exception as e:
            raise TransactionError(f"Transaction failed: {e}")

# Example usage
if __name__ == "__main__":
    horizon_url = "https://horizon-testnet.stellar.org"  # Change to mainnet URL for production
    secret_key = "YOUR_SECRET_KEY"

    try:
        stellar_nexus = PiStellarNexus(horizon_url, secret_key)
        print(f"Connected to Stellar network. Balance: {stellar_nexus.get_balance()}")

        # Example transaction
        to_address = "GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  # Replace with a valid Stellar address
        amount = 10.0  # Amount in XLM
        response = stellar_nexus.create_transaction(to_address, amount)
        print(f"Transaction successful! Response: {response}")

    except ConnectionError as e:
        print(f"Connection error: {e}")
    except TransactionError as e:
        print(f"Transaction error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
