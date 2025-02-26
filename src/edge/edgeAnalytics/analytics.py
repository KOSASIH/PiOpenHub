# edgeAnalytics/analytics.py

import pandas as pd

def perform_analytics(data):
    """Perform real-time analytics on the processed data."""
    print("Performing analytics...")
    
    # Example analytics: Calculate basic statistics
    analytics_results = {
        "mean": data.mean().to_dict(),
        "std": data.std().to_dict(),
        "min": data.min().to_dict(),
        "max": data.max().to_dict(),
        "count": data.count().to_dict()
    }
    
    print("Analytics results:")
    for key, value in analytics_results.items():
        print(f"{key.capitalize()}: {value}")

    return analytics_results

def perform_custom_analytics(data):
    """Perform custom analytics based on specific requirements."""
    # Example: Calculate the correlation matrix
    correlation_matrix = data.corr()
    print("Correlation matrix:")
    print(correlation_matrix)
    
    return correlation_matrix
