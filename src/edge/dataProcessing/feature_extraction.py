import pandas as pd

def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    """Extract features from the input DataFrame."""
    # Example: Create a new feature based on existing ones
    df['temperature_humidity_ratio'] = df['temperature'] / df['humidity']
    return df

# Example usage
if __name__ == "__main__":
    # Sample feature extraction
    sample_data = {
        'temperature': [22.5, 23.0, 22.5, 22.0],
        'humidity': [30, 35, 30, 32]
    }
    df = pd.DataFrame(sample_data)
    feature_df = extract_features(df)
    print("DataFrame with Extracted Features:\n", feature_df)
