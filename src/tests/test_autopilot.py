# tests/test_autopilot.py

import unittest
from autopilotService import AutopilotService
import pandas as pd

class TestAutopilotService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Sample data for testing
        cls.data = pd.DataFrame({
            'feature1': [1, 2, 3, 4, 5],
            'feature2': [5, 4, 3, 2, 1],
            'target': [0, 1, 0, 1, 0]
        })
        cls.data.to_csv('test_data.csv', index=False)
        cls.service = AutopilotService('test_data.csv')

    def test_load_data(self):
        self.service.load_data()
        self.assertIsNotNone(self.service.data)

    def test_preprocess_data(self):
        self.service.load_data()
        self.service.preprocess_data()
        self.assertEqual(self.service.data.shape[0], 5)  # Check if data is still there

    def test_train_model(self):
        self.service.load_data()
        self.service.preprocess_data()
        self.service.train_model(epochs=10)
        self.assertIsNotNone(self.service.model)

    def test_predict(self):
        self.service.load_data()
        self.service.preprocess_data()
        self.service.train_model(epochs=10)
        predictions = self.service.predict([[1, 5]])
        self.assertIn(predictions[0], [0, 1])  # Check if prediction is binary

if __name__ == '__main__':
    unittest.main()
