# piSmartContracts/config.py

import os

class Config:
    """Configuration class for smart contract management."""
    
    # Ethereum node URL
    ETH_NODE_URL = os.getenv('ETH_NODE_URL', 'https://your-ethereum-node-url')

    # Default account for transactions
    DEFAULT_ACCOUNT = os.getenv('DEFAULT_ACCOUNT', '0xYourDefaultAccount')

    # Private key for signing transactions
    PRIVATE_KEY = os.getenv('PRIVATE_KEY', 'your_private_key')

    # Gas price for transactions (in wei)
    GAS_PRICE = int(os.getenv('GAS_PRICE', 20000000000))  # Default to 20 Gwei

    # Gas limit for transactions
    GAS_LIMIT = int(os.getenv('GAS_LIMIT', 3000000))  # Default gas limit

    @staticmethod
    def validate_config():
        """Validate the configuration settings."""
        required_vars = [
            'ETH_NODE_URL',
            'DEFAULT_ACCOUNT',
            'PRIVATE_KEY'
        ]
        for var in required_vars:
            if not os.getenv(var):
                raise ValueError(f"Missing required environment variable: {var}")

# Validate the configuration upon import
Config.validate_config()
