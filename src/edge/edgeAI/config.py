# edgeAI/config.py

import os

class Config:
    """Configuration class for edge AI."""
    
    # Path to the model file
    MODEL_PATH = os.getenv('MODEL_PATH', 'models/edge_model.pkl')
    
    # Path to save inference results
    RESULTS_PATH = os.getenv('RESULTS_PATH', 'results/inference_results.json')

    @staticmethod
    def validate():
        """Validate the configuration settings."""
        if not os.path.exists(Config.MODEL_PATH):
            raise ValueError("Invalid MODEL_PATH. Ensure the model file exists.")
        if not os.path.exists(os.path.dirname(Config.RESULTS_PATH)):
            raise ValueError("Invalid RESULTS_PATH. Ensure the directory exists.")

# Example usage
if __name__ == "__main__":
    try:
        Config.validate()
        print("Configuration is valid.")
    except ValueError as e:
        print(f"Configuration error: {e}")
