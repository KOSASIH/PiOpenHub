# quantumNetworking/config.py

import os

class Config:
    """Configuration class for quantum networking."""
    
    # Path to save networking results
    RESULTS_PATH = os.getenv('RESULTS_PATH', 'results/networking_results.json')

    @staticmethod
    def validate():
        """Validate the configuration settings."""
        if not os.path.exists(os.path.dirname(Config.RESULTS_PATH)):
            raise ValueError("Invalid RESULTS_PATH. Ensure the directory exists.")

# Example usage
if __name__ == "__main__":
    try:
        Config.validate()
        print("Configuration is valid.")
    except ValueError as e:
        print(f"Configuration error: {e}")
