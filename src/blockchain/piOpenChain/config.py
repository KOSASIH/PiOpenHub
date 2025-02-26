class Config:
    """Configuration settings for the PiOpenChain blockchain."""

    # Network settings
    HOST = '127.0.0.1'  # Default host for the blockchain node
    PORT = 5000          # Default port for the blockchain node
    MAX_CONNECTIONS = 5  # Maximum number of simultaneous connections

    # Blockchain settings
    DIFFICULTY = 4       # Difficulty level for mining (number of leading zeros)
    MINING_REWARD = 50   # Reward for mining a new block
    GENESIS_BLOCK_DATA = "Genesis Block"  # Data for the genesis block

    # Transaction settings
    TRANSACTION_FEE = 0.01  # Transaction fee for processing transactions

    # Smart contract settings
    MAX_CONTRACT_SIZE = 1024  # Maximum size of smart contract code in bytes

    # Logging settings
    LOGGING_LEVEL = 'INFO'  # Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    # Other settings
    VERSION = "1.0.0"  # Version of the blockchain software

# Example usage
if __name__ == "__main__":
    print("PiOpenChain Configuration:")
    print(f"Host: {Config.HOST}")
    print(f"Port: {Config.PORT}")
    print(f"Difficulty: {Config.DIFFICULTY}")
    print(f"Mining Reward: {Config.MINING_REWARD}")
    print(f"Transaction Fee: {Config.TRANSACTION_FEE}")
    print(f"Smart Contract Max Size: {Config.MAX_CONTRACT_SIZE}")
    print(f"Logging Level: {Config.LOGGING_LEVEL}")
    print(f"Version: {Config.VERSION}")
