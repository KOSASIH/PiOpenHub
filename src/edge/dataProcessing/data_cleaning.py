import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the input DataFrame by handling missing values and duplicates."""
    # Drop duplicates
    df = df.drop_duplicates()
    
    # Fill missing values (example: fill with mean for numerical columns)
    for column in df.select_dtypes(include=['float64', 'int64']).columns:
        df[column].fillna(df[column].mean(), inplace=True)
    
    return df

# Example usage
if __name__ == "__main__":
    # Sample data cleaning
    sample_data = {
        'temperature': [22.5, None, 23.0, 22.5, 22.0],
        'humidity': [30, 35, None, 30, 32]
    }
    df = pd.DataFrame(sample_data)
    cleaned_df = clean_data(df)
    print("Cleaned DataFrame:\n", cleaned_df)
