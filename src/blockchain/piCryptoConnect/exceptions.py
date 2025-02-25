# exceptions.py

class BlockchainError(Exception):
    """Base class for exceptions in this module."""
    pass

class ConnectionError(BlockchainError):
    """Exception raised for errors in the connection to the blockchain."""
    pass

class TransactionError(BlockchainError):
    """Exception raised for errors in transaction processing."""
    pass

class InsufficientFundsError(TransactionError):
    """Exception raised when there are insufficient funds for a transaction."""
    pass
