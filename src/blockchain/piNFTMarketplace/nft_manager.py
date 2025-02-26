# piNFTMarketplace/nft_manager.py

import json
from web3 import Web3
from .config import Config
from .nft_interactor import NFTInteractor

class NFTManager:
    """Class to manage NFT operations such as minting, listing, and purchasing."""

    def __init__(self):
        # Initialize Web3 connection
        self.web3 = Web3(Web3.HTTPProvider(Config.INFURA_URL))
        if not self.web3.isConnected():
            raise Exception("Failed to connect to the Ethereum network.")
        
        # Initialize the NFT interactor
        self.nft_interactor = NFTInteractor(Config.NFT_CONTRACT_ADDRESS)

    def mint_nft(self, token_uri):
        """Mint a new NFT with the given token URI."""
        try:
            tx_hash = self.nft_interactor.send_transaction('mint', token_uri)
            return tx_hash.hex()  # Return the transaction hash
        except Exception as e:
            print(f"Error minting NFT: {e}")
            return None

    def list_nft(self, token_id, price):
        """List an NFT for sale."""
        try:
            tx_hash = self.nft_interactor.send_transaction('listForSale', token_id, self.web3.toWei(price, 'ether'))
            return tx_hash.hex()  # Return the transaction hash
        except Exception as e:
            print(f"Error listing NFT: {e}")
            return None

    def purchase_nft(self, token_id):
        """Purchase an NFT."""
        try:
            tx_hash = self.nft_interactor.send_transaction('purchase', token_id)
            return tx_hash.hex()  # Return the transaction hash
        except Exception as e:
            print(f"Error purchasing NFT: {e}")
            return None

    def get_nft_details(self, token_id):
        """Get details of an NFT."""
        try:
            details = self.nft_interactor.call_function('getNFTDetails', token_id)
            return details
        except Exception as e:
            print(f"Error retrieving NFT details: {e}")
            return None

# Example usage
if __name__ == "__main__":
    nft_manager = NFTManager()

    # Mint a new NFT
    token_uri = "https://example.com/metadata/1"
    mint_tx_hash = nft_manager.mint_nft(token_uri)
    print(f"Minted NFT transaction hash: {mint_tx_hash}")

    # List the NFT for sale
    token_id = 1
    price = 0.1  # Price in Ether
    list_tx_hash = nft_manager.list_nft(token_id, price)
    print(f"Listed NFT transaction hash: {list_tx_hash}")

    # Purchase the NFT
    purchase_tx_hash = nft_manager.purchase_nft(token_id)
    print(f"Purchase NFT transaction hash: {purchase_tx_hash}")

    # Get NFT details
    nft_details = nft_manager.get_nft_details(token_id)
    print(f"NFT Details: {nft_details}")
