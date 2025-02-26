# autoML/data_preprocessing.py

import pandas as pd
from sklearn.model_selection import train_test_split
from .config import Config

def load_data():
    """Load the dataset from the specified path."""
    try:
        data = pd.read_csv(Config.DATA_PATH)
        print(f"Data loaded successfully from {Config.DATA_PATH}")
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Dataset not found at {Config.DATA_PATH}. Please check the path.")
    except Exception as e:
        raise Exception(f"Error loading data: {e}")

def preprocess_data(data):
    """Preprocess the data for modeling."""
    # Example preprocessing steps
    print("Starting data preprocessing...")
    
    # Drop missing values
    data = data.dropna()
    print("Dropped missing values.")

    # Separate features and target variable
    X = data.drop(columns=[Config.TARGET_COLUMN])
    y = data[Config.TARGET_COLUMN]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=Config.TEST_SIZE, random_state=Config.RANDOM_STATE)
    print(f"Data split into training and testing sets with test size: {Config.TEST_SIZE}")

    return X_train, X_test, y_train, y_test
