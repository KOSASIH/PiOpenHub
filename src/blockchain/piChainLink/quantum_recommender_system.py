from qiskit import QuantumCircuit, Aer, execute
import numpy as np

class QuantumRecommenderSystem:
    def __init__(self, num_items):
        self.num_items = num_items
        self.backend = Aer.get_backend('statevector_simulator')

    def create_circuit(self, user_preferences):
        """Create a quantum circuit for the recommender system."""
        qc = QuantumCircuit(self.num_items)

        # Encode user preferences into the quantum circuit
        for i in range(len(user_preferences)):
            if user_preferences[i] > 0:  # If the user likes the item
                qc.x(i)  # Apply X gate to indicate preference

        return qc

    def run(self, user_preferences):
        """Run the quantum recommender system circuit."""
        qc = self.create_circuit(user_preferences)
        qc.measure_all()  # Measure all qubits
        job = execute(qc, self.backend, shots=1024)
        result = job.result()
        counts = result.get_counts()
        return counts

# Example usage
if __name__ == "__main__":
    # Example user preferences (1: like, 0: dislike)
    user_preferences = [1, 0, 1, 0, 1]  # User likes items 0, 2, and 4

    # Initialize the quantum recommender system
    num_items = len(user_preferences)
    recommender = QuantumRecommenderSystem(num_items)

    # Run the recommender system
    counts = recommender.run(user_preferences)
    print(f"Recommendation counts: {counts}")
