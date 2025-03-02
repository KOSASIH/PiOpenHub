# tests/test_analytics.py

import unittest
import pandas as pd
from analyticsService import AnalyticsService

class TestAnalyticsService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Sample data for testing
        cls.data = pd.DataFrame({
            'feature1': [1, 2, 3, 4, 5],
            'feature2': [5, 4, 3, 2, 1],
            'target': [0, 1, 0, 1, 0]
        })
        cls.service = AnalyticsService(cls.data)

    def test_generate_summary_statistics(self):
        summary = self.service.generate_summary_statistics()
        self.assertIn('feature1', summary.columns)

    def test_correlation_matrix(self):
        self.service.correlation_matrix()  # This will plot, but we can check if it runs without error

    def test_generate_histogram(self):
        try:
            self.service.generate_histogram('feature1')  # Should run without error
        except Exception as e:
            self.fail(f"generate_histogram raised Exception: {e}")

    def test_generate_report(self):
        report = self.service.generate_report()
        self.assertIn('summary_statistics', report)

if __name__ == '__main__':
    unittest.main()
