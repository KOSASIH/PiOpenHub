# edgeAnalytics/data_ingestion.py

import pandas as pd
import time
from .config import Config

def ingest_data():
    """Ingest data from the specified source at regular intervals."""
    while True:
        try:
            # Read the data from the specified source
            data = pd.read_csv(Config.DATA_SOURCE)
            print(f"Data ingested successfully from {Config.DATA_SOURCE}")
            return data
        except FileNotFoundError:
            print(f"File not found at {Config.DATA_SOURCE}. Retrying in {Config.SAMPLING_RATE} seconds...")
            time.sleep(Config.SAMPLING_RATE)  # Wait before retrying
        except Exception as e:
            print(f"Error ingesting data: {e}. Retrying in {Config.SAMPLING_RATE} seconds...")
            time.sleep(Config.SAMPLING_RATE)  # Wait before retrying
