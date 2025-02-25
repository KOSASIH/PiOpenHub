import unittest
import pandas as pd
from src.main.services.analyticsService import AnalyticsService  # Adjust the import based on your project structure

class TestAnalyticsService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the Analytics service before any tests run."""
        cls.analytics_service = AnalyticsService()

    def test_data_processing(self):
        """Test the data processing method."""
        raw_data = {
            'user_id': [1, 2, 3, 4],
            'purchase_amount': [100, 200, 300, 400],
            'timestamp': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04']
        }
        df = pd.DataFrame(raw_data)
        processed_data = self.analytics_service.process_data(df)
        
        # Check if the processed data has the expected columns
        expected_columns = ['user_id', 'purchase_amount', 'timestamp', 'purchase_category']
        self.assertTrue(all(col in processed_data.columns for col in expected_columns), "Processed data should contain expected columns.")

    def test_report_generation(self):
        """Test the report generation method."""
        processed_data = pd.DataFrame({
            'user_id': [1, 2, 3, 4],
            'purchase_amount': [100, 200, 300, 400],
            'timestamp': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04'],
            'purchase_category': ['A', 'B', 'A', 'B']
        })
        report = self.analytics_service.generate_report(processed_data)
        
        # Check if the report contains the expected keys
        expected_keys = ['total_sales', 'category_distribution']
        self.assertTrue(all(key in report for key in expected_keys), "Report should contain total_sales and category_distribution.")

    def test_statistical_calculations(self):
        """Test statistical calculations."""
        data = [100, 200, 300, 400, 500]
        mean = self.analytics_service.calculate_mean(data)
        median = self.analytics_service.calculate_median(data)
        
        self.assertEqual(mean, 300, "Mean should be 300.")
        self.assertEqual(median, 300, "Median should be 300.")

    def test_invalid_data_processing(self):
        """Test data processing with invalid input."""
        invalid_data = None  # Example of invalid input
        with self.assertRaises(ValueError, msg="Processing should raise ValueError for invalid input data."):
            self.analytics_service.process_data(invalid_data)

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests have run."""
        cls.analytics_service = None  # Clean up the analytics service instance

if __name__ == '__main__':
    unittest.main()
