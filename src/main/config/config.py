import os

class Config:
    """Configuration settings for the Flask application."""
    
    # General settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT settings
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'your_jwt_secret_key'
    
    # CORS settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS') or '*'
    
    # Logging settings
    LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL') or 'INFO'
