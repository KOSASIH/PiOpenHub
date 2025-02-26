# autoML/config.py

import os

class Config:
    """Configuration class for AutoML processes."""
    
    # Path to the dataset
    DATA_PATH = os.getenv('DATA_PATH', 'data/dataset.csv')
    
    # Target column name in the dataset
    TARGET_COLUMN = os.getenv('TARGET_COLUMN', 'target')
    
    # Path to save the trained model
    MODEL_SAVE_PATH = os.getenv('MODEL_SAVE_PATH', 'models/best_model.pkl')
    
    # Test size for train-test split
    TEST_SIZE = float(os.getenv('TEST_SIZE', 0.2))
    
    # Random state for reproducibility
    RANDOM_STATE = int(os.getenv('RANDOM_STATE', 42))

    @staticmethod
    def validate():
        """Validate the configuration settings."""
        if not os.path.exists(Config.DATA_PATH):
            raise ValueError("Invalid DATA_PATH. Ensure the dataset file exists.")
        if not isinstance(Config.TEST_SIZE, float) or not (0 < Config.TEST_SIZE < 1):
            raise ValueError("TEST_SIZE must be a float between 0 and 1.")
        if not isinstance(Config.RANDOM_STATE, int):
            raise ValueError("RANDOM_STATE must be an integer.")

# Example usage
if __name__ == "__main__":
    try:
        Config.validate()
        print("Configuration is valid.")
    except ValueError as e:
        print(f"Configuration error: {e}")
