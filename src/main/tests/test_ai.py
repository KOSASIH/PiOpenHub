import unittest
import numpy as np
from src.main.services.aiService import AIService  # Adjust the import based on your project structure

class TestAIService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the AI service and load the model before any tests run."""
        cls.ai_service = AIService(model_path='path/to/your/model')  # Provide the correct model path
        cls.ai_service.load_model()

    def test_model_loading(self):
        """Test if the model loads correctly."""
        self.assertIsNotNone(self.ai_service.model, "Model should be loaded successfully.")

    def test_inference(self):
        """Test the inference method of the AI service."""
        input_data = np.array([[1.0, 2.0, 3.0]])  # Example input data
        expected_output = np.array([[0.5]])  # Replace with the expected output based on your model
        output = self.ai_service.infer(input_data)
        np.testing.assert_array_almost_equal(output, expected_output, decimal=2, err_msg="Inference output does not match expected output.")

    def test_inference_with_invalid_data(self):
        """Test inference with invalid input data."""
        invalid_input_data = np.array([[None]])  # Example of invalid input
        with self.assertRaises(ValueError, msg="Inference should raise ValueError for invalid input data."):
            self.ai_service.infer(invalid_input_data)

    def test_model_evaluation(self):
        """Test the model evaluation method."""
        test_data = np.array([[1.0, 2.0, 3.0]])  # Example test data
        test_labels = np.array([[0.5]])  # Example test labels
        evaluation_result = self.ai_service.evaluate(test_data, test_labels)
        self.assertIsInstance(evaluation_result, dict, "Evaluation result should be a dictionary.")
        self.assertIn('accuracy', evaluation_result, "Evaluation result should contain accuracy.")
        self.assertGreaterEqual(evaluation_result['accuracy'], 0.0, "Accuracy should be non-negative.")

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests have run."""
        cls.ai_service.unload_model()  # Assuming you have a method to unload the model

if __name__ == '__main__':
    unittest.main()
