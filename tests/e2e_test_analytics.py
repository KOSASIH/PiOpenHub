import unittest
import requests

class TestAnalyticsEndToEnd(unittest.TestCase):
    BASE_URL = "http://localhost:5000"  # Change to your API base URL

    def test_analytics_report(self):
        """Test the analytics report generation endpoint."""
        response = requests.get(f"{self.BASE_URL}/api/analytics/report")
        self.assertEqual(response.status_code, 200)
        
        report = response.json()
        self.assertIn("total_sales", report)
        self.assertIn("category_distribution", report)

    def test_analytics_data(self):
        """Test the analytics data retrieval endpoint."""
        response = requests.get(f"{self.BASE_URL}/api/analytics/data")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIsInstance(data, list)  # Assuming the data is a list of records

if __name__ == "__main__":
    unittest.main()
