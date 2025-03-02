# analyticsService.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class AnalyticsService:
    def __init__(self, data):
        self.data = data

    def generate_summary_statistics(self):
        """Generate summary statistics for the dataset."""
        try:
            summary = self.data.describe()
            logging.info("Summary statistics generated successfully.")
            return summary
        except Exception as e:
            logging.error(f"Error generating summary statistics: {e}")
            return None

    def correlation_matrix(self):
        """Calculate and visualize the correlation matrix."""
        try:
            corr = self.data.corr()
            plt.figure(figsize=(10, 8))
            sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', square=True)
            plt.title("Correlation Matrix")
            plt.show()
            logging.info("Correlation matrix visualized successfully.")
        except Exception as e:
            logging.error(f"Error calculating correlation matrix: {e}")

    def generate_histogram(self, column):
        """Generate a histogram for a specific column."""
        try:
            plt.figure(figsize=(10, 6))
            sns.histplot(self.data[column], bins=30, kde=True)
            plt.title(f"Histogram of {column}")
            plt.xlabel(column)
            plt.ylabel("Frequency")
            plt.show()
            logging.info(f"Histogram for {column} generated successfully.")
        except Exception as e:
            logging.error(f"Error generating histogram for {column}: {e}")

    def generate_report(self):
        """Generate a comprehensive report of the dataset."""
        try:
            report = {
                "summary_statistics": self.generate_summary_statistics(),
                "correlation_matrix": self.data.corr().to_dict()
            }
            logging.info("Report generated successfully.")
            return report
        except Exception as e:
            logging.error(f"Error generating report: {e}")
            return None

# Example usage
if __name__ == "__main__":
    # Load your dataset
    data_path = 'data.csv'  # Replace with your actual data source
    data = pd.read_csv(data_path)

    # Initialize the analytics service
    analytics_service = AnalyticsService(data)

    # Generate summary statistics
    summary_stats = analytics_service.generate_summary_statistics()
    print("Summary Statistics:\n", summary_stats)

    # Generate correlation matrix
    analytics_service.correlation_matrix()

    # Generate histogram for a specific column
    analytics_service.generate_histogram('target')  # Replace 'target' with your actual column name

    # Generate a comprehensive report
    report = analytics_service.generate_report()
    print("Generated Report:\n", report)
