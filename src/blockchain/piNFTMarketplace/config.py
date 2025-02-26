# piNFTMarketplace/config.py

import os

class Config:
    """Configuration class for NFT Marketplace integration."""
    
    # Ethereum network settings
    INFURA_URL = os.getenv('INFURA_URL', 'https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID')
    PRIVATE_KEY = os.getenv('PRIVATE_KEY', 'your_private_key')
    ACCOUNT_ADDRESS = os.getenv('ACCOUNT_ADDRESS', 'your_account_address')
    
    # NFT contract settings
    NFT_CONTRACT_ADDRESS = os.getenv('NFT_CONTRACT_ADDRESS', '0xYourNFTContractAddress')
    NFT_CONTRACT_ABI = os.getenv('NFT_CONTRACT_ABI', 'path/to/your/nft_contract.abi')

    @staticmethod
    def validate():
        """Validate the configuration settings."""
        if not Config.INFURA_URL.startswith('https://'):
            raise ValueError("Invalid INFURA_URL. It should start with 'https://'.")
        if not Config.PRIVATE_KEY or len(Config.PRIVATE_KEY) < 64:
            raise ValueError("Invalid PRIVATE_KEY. Ensure it is a valid Ethereum private key.")
        if not Config.ACCOUNT_ADDRESS.startswith('0x') or len(Config.ACCOUNT_ADDRESS) != 42:
            raise ValueError("Invalid ACCOUNT_ADDRESS. Ensure it is a valid Ethereum address.")
        if not Config.NFT_CONTRACT_ADDRESS.startswith('0x') or len(Config.NFT_CONTRACT_ADDRESS) != 42:
            raise ValueError("Invalid NFT_CONTRACT_ADDRESS. Ensure it is a valid Ethereum address.")
        if not os.path.exists(Config.NFT_CONTRACT_ABI):
            raise ValueError("Invalid NFT_CONTRACT_ABI path. Ensure the ABI file exists.")

# Example usage
if __name__ == "__main__":
    try:
        Config.validate()
        print("Configuration is valid.")
    except ValueError as e:
        print(f"Configuration error: {e}")
