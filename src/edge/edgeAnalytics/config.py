# edgeAnalytics/config.py

import os

class Config:
    """Configuration class for edge analytics."""
    
    # Path to the data source
    DATA_SOURCE = os.getenv('DATA_SOURCE', 'data/stream_data.csv')
    
    # Path to save analytics results
    RESULTS_PATH = os.getenv('RESULTS_PATH', 'results/analytics_results.json')
    
    # Sampling rate for data ingestion (in seconds)
    SAMPLING_RATE = int(os.getenv('SAMPLING_RATE', 5))

    @staticmethod
    def validate():
        """Validate the configuration settings."""
        if not os.path.exists(Config.DATA_SOURCE):
            raise ValueError("Invalid DATA_SOURCE. Ensure the data source file exists.")
        if not os.path.exists(os.path.dirname(Config.RESULTS_PATH)):
            raise ValueError("Invalid RESULTS_PATH. Ensure the directory exists.")

# Example usage
if __name__ == "__main__":
    try:
        Config.validate()
        print("Configuration is valid.")
    except ValueError as e:
        print(f"Configuration error: {e}")
