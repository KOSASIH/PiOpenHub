from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    recipient_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_hash = Column(String(64), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    sender = relationship("User", foreign_keys=[sender_id])
    recipient = relationship("User", foreign_keys=[recipient_id])

    def __repr__(self):
        return f"<Transaction(id={self.id}, sender_id={self.sender_id}, recipient_id={self.recipient_id}, amount={self.amount}, transaction_hash={self.transaction_hash})>"

# Database setup
DATABASE_URL = "sqlite:///transactions.db"  # Example SQLite database URL
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def create_transaction(sender_id, recipient_id, amount, transaction_hash):
    """Create a new transaction in the database."""
    session = Session()
    try:
        new_transaction = Transaction(sender_id=sender_id, recipient_id=recipient_id, amount=amount, transaction_hash=transaction_hash)
        session.add(new_transaction)
        session.commit()
        logging.info(f"Transaction created: {new_transaction}")
        return new_transaction
    except Exception as e:
        session.rollback()
        logging.error(f"Error creating transaction: {e}")
        return None
    finally:
        session.close()

def get_transaction_by_id(transaction_id):
    """Retrieve a transaction by its ID."""
    session = Session()
    try:
        transaction = session.query(Transaction).filter_by(id=transaction_id).first()
        logging.info(f"Retrieved transaction: {transaction}")
        return transaction
    except Exception as e:
        logging.error(f"Error retrieving transaction: {e}")
        return None
    finally:
        session.close()

def get_transactions_by_user(user_id):
    """Retrieve all transactions for a specific user."""
    session = Session()
    try:
        transactions = session.query(Transaction).filter((Transaction.sender_id == user_id) | (Transaction.recipient_id == user_id)).all()
        logging.info(f"Retrieved transactions for user {user_id}: {transactions}")
        return transactions
    except Exception as e:
        logging.error(f"Error retrieving transactions for user {user_id}: {e}")
        return None
    finally:
        session.close()

# Example usage
if __name__ == "__main__":
    # Create a new transaction
    transaction = create_transaction(sender_id=1, recipient_id=2, amount=0.05, transaction_hash="abc123hash")

    # Retrieve a specific transaction
    transaction_data = get_transaction_by_id(1)

    # Retrieve transactions for a specific user
    user_transactions = get_transactions_by_user(1)
