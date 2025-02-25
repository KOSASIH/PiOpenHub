import pandas as pd

def aggregate_data(dfs: list) -> pd.DataFrame:
    """Aggregate a list of DataFrames into a single DataFrame."""
    return pd.concat(dfs, ignore_index=True).groupby(['temperature']).mean().reset_index()

# Example usage
if __name__ == "__main__":
    # Sample data aggregation
    data1 = pd.DataFrame({'temperature': [22.5, 23.0], 'humidity': [30, 35]})
    data2 = pd.DataFrame({'temperature': [22.5, 22.0], 'humidity': [30, 32]})
    aggregated_df = aggregate_data([data1, data2])
    print("Aggregated DataFrame:\n", aggregated_df)
