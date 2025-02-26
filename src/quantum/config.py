# quantum/config.py

import os

class Config:
    """Configuration class for quantum computing."""
    
    # Path to save quantum algorithm results
    RESULTS_PATH = os.getenv('RESULTS_PATH', 'results/quantum_results.json')

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
