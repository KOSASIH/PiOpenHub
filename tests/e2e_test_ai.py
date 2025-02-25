import unittest
import requests

class TestAIEndToEnd(unittest.TestCase):
    BASE_URL = "http://localhost:5000"  # Change to your API base URL

    def test_model_inference(self):
        """Test the AI model inference endpoint."""
        input_data = {
            "texts": ["I love programming!", "The weather is terrible today."]
        }
        response = requests.post(f"{self.BASE_URL}/api/inference", json=input_data)
        self.assertEqual(response.status_code, 200)
        
        predictions = response.json().get("predictions")
        self.assertIsInstance(predictions, list)
        self.assertEqual(len(predictions), len(input_data["texts"]))

if __name__ == "__main__":
    unittest.main()
