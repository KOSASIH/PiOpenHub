# piChainLink/config.py

import os

class Config:
    """Configuration class for Chainlink integration."""
    
    # Chainlink Node URL
    CHAINLINK_NODE_URL = os.getenv('CHAINLINK_NODE_URL', 'https://your-chainlink-node-url')

    # Chainlink Oracle Address
    CHAINLINK_ORACLE_ADDRESS = os.getenv('CHAINLINK_ORACLE_ADDRESS', '0xYourOracleAddress')

    # Chainlink Job ID
    CHAINLINK_JOB_ID = os.getenv('CHAINLINK_JOB_ID', 'your_job_id')

    # Private Key for signing requests
    CHAINLINK_PRIVATE_KEY = os.getenv('CHAINLINK_PRIVATE_KEY', 'your_private_key')

    # Optional: Timeout settings for requests
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 10))  # Default to 10 seconds

    # Optional: Log level for debugging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    @staticmethod
    def validate_config():
        """Validate the configuration settings."""
        required_vars = [
            'CHAINLINK_NODE_URL',
            'CHAINLINK_ORACLE_ADDRESS',
            'CHAINLINK_JOB_ID',
            'CHAINLINK_PRIVATE_KEY'
        ]
        for var in required_vars:
            if not os.getenv(var):
                raise ValueError(f"Missing required environment variable: {var}")

# Validate the configuration upon import
Config.validate_config()
