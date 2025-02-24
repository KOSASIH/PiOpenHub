from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
import bcrypt
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email}, is_active={self.is_active})>"

    @staticmethod
    def hash_password(password):
        """Hash a password for storing."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    @staticmethod
    def verify_password(stored_password, provided_password):
        """Verify a stored password against one provided by user."""
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)

# Database setup
DATABASE_URL = "sqlite:///users.db"  # Example SQLite database URL
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def create_user(username, email, password):
    """Create a new user in the database."""
    session = Session()
    try:
        password_hash = User.hash_password(password)
        new_user = User(username=username, email=email, password_hash=password_hash)
        session.add(new_user)
        session.commit()
        logging.info(f"User created: {new_user}")
        return new_user
    except Exception as e:
        session.rollback()
        logging.error(f"Error creating user: {e}")
        return None
    finally:
        session.close()

def get_user_by_username(username):
    """Retrieve a user by username."""
    session = Session()
    try:
        user = session.query(User).filter_by(username=username).first()
        logging.info(f"Retrieved user: {user}")
        return user
    except Exception as e:
        logging.error(f"Error retrieving user: {e}")
        return None
    finally:
        session.close()

def authenticate_user(username, password):
    """Authenticate a user by username and password."""
    user = get_user_by_username(username)
    if user and User.verify_password(user.password_hash, password):
        logging.info(f"User authenticated: {user.username}")
        return user
    else:
        logging.warning("Authentication failed.")
        return None

# Example usage
if __name__ == "__main__":
    # Create a new user
    create_user("john_doe", "john@example.com", "securepassword123")

    # Authenticate the user
    authenticated_user = authenticate_user("john_doe", "securepassword123")
    if authenticated_user:
        print(f"Authenticated user: {authenticated_user.username}")
