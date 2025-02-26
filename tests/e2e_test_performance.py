import unittest
import time
import numpy as np
from quantumAI.quantum_machine_learning import run_quantum_ml
from quantumAI.quantum_neural_network import run_quantum_neural_network

class TestQuantumPerformanceMetrics(unittest.TestCase):

    def test_quantum_machine_learning_performance(self):
        """Test the performance of the quantum machine learning algorithm."""
        print("Testing Quantum Machine Learning Performance...")
        
        # Generate example data for testing
        example_data = [np.pi / 4, np.pi / 2]  # Example angles for rotation
        
        # Measure the execution time
        start_time = time.time()
        result = run_quantum_ml(example_data)
        execution_time = time.time() - start_time
        
        # Check that the result is not empty
        self.assertTrue(result, "Quantum machine learning did not return a result.")
        
        # Print performance metrics
        print(f"Execution Time for Quantum Machine Learning: {execution_time:.4f} seconds")
        print("Quantum Machine Learning performance test passed.")

    def test_quantum_neural_network_performance(self):
        """Test the performance of the quantum neural network."""
        print("Testing Quantum Neural Network Performance...")
        
        # Generate example input data
        example_input = [0.5, 0.5]  # Placeholder for input data
        
        # Measure the execution time
        start_time = time.time()
        result = run_quantum_neural_network(example_input)
        execution_time = time.time() - start_time
        
        # Check that the result is not empty
        self.assertTrue(result, "Quantum neural network did not return a result.")
        
        # Print performance metrics
        print(f"Execution Time for Quantum Neural Network: {execution_time:.4f} seconds")
        print("Quantum Neural Network performance test passed.")

if __name__ == "__main__":
    unittest.main()
