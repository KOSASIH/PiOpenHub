# dataProcessingService.py

import pandas as pd
import numpy as np
import logging
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Configure logging
logging.basicConfig(level=logging.INFO)

class DataProcessingService:
    def __init__(self, data_source):
        self.data_source = data_source
        self.data = None
        self.scaler = StandardScaler()

    def load_data(self):
        """Load data from a CSV file or other sources."""
        try:
            if self.data_source.endswith('.csv'):
                self.data = pd.read_csv(self.data_source)
            else:
                raise ValueError("Unsupported data source format. Only CSV is supported.")
            logging.info("Data loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading data: {e}")

    def preprocess_data(self):
        """Preprocess the data for analysis."""
        if self.data is not None:
            try:
                # Handle missing values
                self.data.dropna(inplace=True)

                # Example transformation: Convert categorical variables to dummy variables
                self.data = pd.get_dummies(self.data)

                logging.info("Data preprocessed successfully.")
            except Exception as e:
                logging.error(f"Error preprocessing data: {e}")

    def split_data(self, target_column, test_size=0.2):
        """Split the data into training and testing sets."""
        if self.data is not None:
            try:
                X = self.data.drop(target_column, axis=1)
                y = self.data[target_column]
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
                logging.info("Data split into training and testing sets.")
                return X_train, X_test, y_train, y_test
            except Exception as e:
                logging.error(f"Error splitting data: {e}")
                return None, None, None, None
        else:
            logging.error("Data not loaded. Please load data first.")
            return None, None, None, None

    def scale_data(self, X_train, X_test):
        """Scale the features using StandardScaler."""
        if X_train is not None and X_test is not None:
            try:
                X_train_scaled = self.scaler.fit_transform(X_train)
                X_test_scaled = self.scaler.transform(X_test)
                logging.info("Data scaled successfully.")
                return X_train_scaled, X_test_scaled
            except Exception as e:
                logging.error(f"Error scaling data: {e}")
                return None, None
        else:
            logging.error("Training and testing data must be provided for scaling.")
            return None, None

# Example usage
if __name__ == "__main__":
    # Path to your dataset
    data_source = 'data.csv'  # Replace with your actual data source
    data_processing_service = DataProcessingService(data_source)

    # Load data
    data_processing_service.load_data()

    # Preprocess data
    data_processing_service.preprocess_data()

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = data_processing_service.split_data(target_column='target')

    # Scale the data
    X_train_scaled, X_test_scaled = data_processing_service.scale_data(X_train, X_test)

    # Output the shapes of the processed data
    print(f"Training data shape: {X_train_scaled.shape}, Testing data shape: {X_test_scaled.shape}")
