# edgeAI/data_preprocessing.py

import pandas as pd
import numpy as np

def preprocess_data(data):
    """Preprocess the input data for inference."""
    print("Preprocessing data...")
    
    # Check if the input is a DataFrame
    if isinstance(data, pd.DataFrame):
        # Drop missing values
        data = data.dropna()
        print("Dropped missing values.")

        # Example: Normalize numerical features (if applicable)
        numerical_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        if numerical_cols:
            data[numerical_cols] = (data[numerical_cols] - data[numerical_cols].mean()) / data[numerical_cols].std()
            print("Normalized numerical features.")

        # Convert DataFrame to numpy array for model input
        return data.values
    else:
        raise ValueError("Input data must be a pandas DataFrame.")

# Example usage
if __name__ == "__main__":
    # Example DataFrame
    example_data = pd.DataFrame({
        'feature1': [1.0, 2.0, np.nan, 4.0],
        'feature2': [4.0, 5.0, 6.0, 7.0]
    })

    # Preprocess the example data
    processed_data = preprocess_data(example_data)
    print("Processed data:", processed_data)
