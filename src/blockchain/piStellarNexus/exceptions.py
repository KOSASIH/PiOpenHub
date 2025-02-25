# exceptions.py

class StellarError(Exception):
    """Base class for exceptions in this module."""
    pass

class ConnectionError(StellarError):
    """Exception raised for errors in the connection to the Stellar network."""
    pass

class TransactionError(StellarError):
    """Exception raised for errors in transaction processing."""
    pass

class InsufficientFundsError(TransactionError):
    """Exception raised when there are insufficient funds for a transaction."""
    pass
