# autoML/utils.py

import pandas as pd
import joblib

def load_data(file_path):
    """Load data from a CSV file."""
    try:
        data = pd.read_csv(file_path)
        print(f"Data loaded successfully from {file_path}")
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found at {file_path}. Please check the path.")
    except Exception as e:
        raise Exception(f"Error loading data: {e}")

def save_model(model, model_path):
    """Save the model to the specified path."""
    try:
        joblib.dump(model, model_path)
        print(f"Model saved to {model_path}")
    except Exception as e:
        raise Exception(f"Error saving model: {e}")

def load_model(model_path):
    """Load a model from the specified path."""
    try:
        model = joblib.load(model_path)
        print(f"Model loaded from {model_path}")
        return model
    except FileNotFoundError:
        raise FileNotFoundError(f"Model file not found at {model_path}. Please check the path.")
    except Exception as e:
        raise Exception(f"Error loading model: {e}")

def print_dataframe_info(df):
    """Print basic information about a DataFrame."""
    print("DataFrame Information:")
    print(df.info())
    print("First 5 rows:")
    print(df.head())

# Example usage
if __name__ == "__main__":
    # Example of loading data
    try:
        data = load_data('data/dataset.csv')
        print_dataframe_info(data)
    except Exception as e:
        print(e)
