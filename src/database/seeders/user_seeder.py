# user_seeder.py
from sqlalchemy.orm import Session
from models.user_model import User

def seed_users(session: Session):
    """Seed the database with user data."""
    users = [
        User(username='john_doe', email='john@example.com'),
        User(username='jane_doe', email='jane@example.com'),
    ]
    session.bulk_save_objects(users)
    session.commit()
    print("Users seeded successfully.")
