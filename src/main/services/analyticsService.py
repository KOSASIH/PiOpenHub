import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class AnalyticsService:
    def __init__(self, data):
        """Initialize the AnalyticsService with a DataFrame."""
        if isinstance(data, str):
            self.data = pd.read_csv(data)  # Load data from CSV if a file path is provided
        elif isinstance(data, pd.DataFrame):
            self.data = data
        else:
            raise ValueError("Data must be a DataFrame or a file path to a CSV.")

    def summarize_data(self):
        """Return a summary of the dataset."""
        return self.data.describe()

    def correlation_matrix(self):
        """Calculate and return the correlation matrix of the dataset."""
        return self.data.corr()

    def plot_correlation_matrix(self):
        """Plot the correlation matrix using a heatmap."""
        plt.figure(figsize=(10, 8))
        sns.heatmap(self.correlation_matrix(), annot=True, fmt=".2f", cmap='coolwarm', square=True)
        plt.title('Correlation Matrix')
        plt.show()

    def group_by(self, column, agg_func='mean'):
        """Group the data by a specified column and apply an aggregation function."""
        if agg_func == 'mean':
            return self.data.groupby(column).mean()
        elif agg_func == 'sum':
            return self.data.groupby(column).sum()
        elif agg_func == 'count':
            return self.data.groupby(column).count()
        else:
            raise ValueError("Unsupported aggregation function. Use 'mean', 'sum', or 'count'.")

    def plot_time_series(self, time_column, value_column):
        """Plot a time series graph for the specified columns."""
        self.data[time_column] = pd.to_datetime(self.data[time_column])
        plt.figure(figsize=(12, 6))
        plt.plot(self.data[time_column], self.data[value_column], marker='o')
        plt.title(f'Time Series of {value_column}')
        plt.xlabel(time_column)
        plt.ylabel(value_column)
        plt.grid()
        plt.show()

    def generate_report(self, report_file='analytics_report.txt'):
        """Generate a simple text report of the analytics."""
        with open(report_file, 'w') as f:
            f.write("Data Summary:\n")
            f.write(str(self.summarize_data()))
            f.write("\n\nCorrelation Matrix:\n")
            f.write(str(self.correlation_matrix()))
            f.write("\n\nGroup By Mean:\n")
            f.write(str(self.group_by(self.data.columns[0], 'mean')))  # Group by the first column as an example

# Example usage
if __name__ == "__main__":
    # Load data and create an instance of AnalyticsService
    analytics_service = AnalyticsService('data.csv')

    # Summarize data
    print("Data Summary:")
    print(analytics_service.summarize_data())

    # Plot correlation matrix
    analytics_service.plot_correlation_matrix()

    # Group by a specific column
    print("Grouped Data (Mean):")
    print(analytics_service.group_by('category_column', 'mean'))  # Replace 'category_column' with an actual column name

    # Plot time series
    analytics_service.plot_time_series('date_column', 'value_column')  # Replace with actual column names

    # Generate a report
    analytics_service.generate_report()
    print("Analytics report generated.")
