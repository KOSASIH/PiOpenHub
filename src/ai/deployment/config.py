# ai/deployment/config.py

import os

class Config:
    """Configuration class for AI model deployment."""
    
    # Path to the model file
    MODEL_PATH = os.getenv('MODEL_PATH', 'models/my_model.pkl')
    
    # Flask server settings
    PORT = int(os.getenv('PORT', 5000))
    HOST = os.getenv('HOST', '0.0.0.0')

    @staticmethod
    def validate():
        """Validate the configuration settings."""
        if not os.path.exists(Config.MODEL_PATH):
            raise ValueError("Invalid MODEL_PATH. Ensure the model file exists.")
        if not (0 < Config.PORT < 65536):
            raise ValueError("Invalid PORT. It should be between 1 and 65535.")
        if not Config.HOST:
            raise ValueError("Invalid HOST. It should not be empty.")

# Example usage
if __name__ == "__main__":
    try:
        Config.validate()
        print("Configuration is valid.")
    except ValueError as e:
        print(f"Configuration error: {e}")
