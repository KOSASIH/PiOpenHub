import unittest
from quantumAI.quantum_machine_learning import run_quantum_ml
from quantumAI.quantum_neural_network import run_quantum_neural_network

class TestQuantumFunctionalities(unittest.TestCase):

    def test_quantum_machine_learning(self):
        """Test the quantum machine learning functionality."""
        print("Testing Quantum Machine Learning...")
        
        # Example input data for quantum machine learning
        example_data = [0.5, 0.5]  # Example data for testing
        
        # Run the quantum machine learning algorithm
        result = run_quantum_ml(example_data)
        
        # Check that the result is not empty
        self.assertTrue(result, "Quantum machine learning did not return a result.")
        
        print("Quantum Machine Learning test passed.")

    def test_quantum_neural_network(self):
        """Test the quantum neural network functionality."""
        print("Testing Quantum Neural Network...")
        
        # Example input data for quantum neural network
        example_input = [0.3, 0.7]  # Example data for testing
        
        # Run the quantum neural network
        result = run_quantum_neural_network(example_input)
        
        # Check that the result is not empty
        self.assertTrue(result, "Quantum neural network did not return a result.")
        
        print("Quantum Neural Network test passed.")

if __name__ == "__main__":
    unittest.main()
