# analyticsController.py

from flask import Flask, request, jsonify
from analyticsService import AnalyticsService
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Load your dataset
data_path = 'data.csv'  # Replace with your actual data source
data = pd.read_csv(data_path)

# Initialize the analytics service
analytics_service = AnalyticsService(data)

@app.route('/summary', methods=['GET'])
def summary_statistics():
    """Endpoint to get summary statistics of the dataset."""
    try:
        summary = analytics_service.generate_summary_statistics()
        return jsonify(summary.to_dict()), 200
    except Exception as e:
        logging.error(f"Error generating summary statistics: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/correlation', methods=['GET'])
def correlation_matrix():
    """Endpoint to get the correlation matrix."""
    try:
        analytics_service.correlation_matrix()  # This will display the heatmap
        return jsonify({"message": "Correlation matrix visualized successfully."}), 200
    except Exception as e:
        logging.error(f"Error visualizing correlation matrix: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/histogram', methods=['POST'])
def histogram():
    """Endpoint to generate a histogram for a specific column."""
    try:
        column = request.json.get('column')
        if not column:
            return jsonify({"error": "Column name is required."}), 400
        analytics_service.generate_histogram(column)
        return jsonify({"message": f"Histogram for {column} generated successfully."}), 200
    except Exception as e:
        logging.error(f"Error generating histogram: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/report', methods=['GET'])
def generate_report():
    """Endpoint to generate a comprehensive report of the dataset."""
    try:
        report = analytics_service.generate_report()
        return jsonify(report), 200
    except Exception as e:
        logging.error(f"Error generating report: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
