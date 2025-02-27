import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from qiskit import QuantumCircuit, Aer, execute
from qiskit.circuit.library import ZZFeatureMap
from qiskit.aer import AerSimulator
from qiskit_machine_learning.algorithms import QSVC

class QuantumRecommendationSystem:
    def __init__(self, user_item_matrix):
        self.user_item_matrix = user_item_matrix
        self.similarity_matrix = None

    def compute_similarity(self):
        """Compute cosine similarity between users."""
        self.similarity_matrix = cosine_similarity(self.user_item_matrix)

    def recommend(self, user_index, num_recommendations=5):
        """Recommend items for a given user based on similarity."""
        user_similarities = self.similarity_matrix[user_index]
        similar_users_indices = np.argsort(user_similarities)[::-1][1:]  # Exclude self
        recommendations = []

        for similar_user in similar_users_indices:
            recommended_items = np.where(self.user_item_matrix[similar_user] > 0)[0]
            recommendations.extend(recommended_items)

            if len(recommendations) >= num_recommendations:
                break

        return list(set(recommendations))[:num_recommendations]

    def quantum_transform(self, data):
        """Apply a quantum transformation to the user-item matrix."""
        n, m = data.shape
        qc = QuantumCircuit(n * m)
        qc.initialize(data.flatten().tolist(), range(n * m))
        qc.measure_all()

        # Simulate the circuit
        simulator = Aer.get_backend('qasm_simulator')
        result = execute(qc, backend=simulator, shots=1024).result()
        counts = result.get_counts(qc)

        transformed_data = np.zeros((len(counts), n * m))
        for i, (key, count) in enumerate(counts.items()):
            transformed_data[i] = [int(bit) for bit in key]
        return transformed_data

    def quantum_similarity(self, user_index):
        """Compute quantum-enhanced similarity for a specific user."""
        user_vector = self.user_item_matrix[user_index]
        feature_map = ZZFeatureMap(feature_dimension=len(user_vector), reps=2)
        qc = QuantumCircuit(len(user_vector))
        qc.append(feature_map, range(len(user_vector)))
        qc.initialize(user_vector.tolist(), range(len(user_vector)))
        qc.measure_all()

        # Simulate the circuit
        simulator = Aer.get_backend('aer_simulator')
        result = execute(qc, backend=simulator, shots=1024).result()
        counts = result.get_counts(qc)

        # Calculate similarity based on measurement results
        transformed_vector = np.zeros(len(user_vector))
        for key, count in counts.items():
            index = int(key, 2)
            transformed_vector[index] += count

        return transformed_vector / np.sum(transformed_vector)  # Normalize

# Example usage
if __name__ == "__main__":
    # Simulated user-item interaction matrix (users x items)
    user_item_matrix = np.array([[5, 0, 0, 1, 0],
                                  [4, 0, 0, 1, 0],
                                  [0, 0, 5, 0, 0],
                                  [0, 3, 0, 0, 0],
                                  [0, 0, 0, 4, 5]])

    recommender = QuantumRecommendationSystem(user_item_matrix)
    recommender.compute_similarity()
    recommendations = recommender.recommend(user_index=0, num_recommendations=3)
    print("Recommendations for User 0:", recommendations)

    # Apply quantum transformation
    transformed_data = recommender.quantum_transform(user_item_matrix)
    print("Transformed User-Item Matrix:\n", transformed_data)

    # Compute quantum-enhanced similarity for User 0
    quantum_sim = recommender.quantum_similarity(user_index=0)
    print("Quantum Enhanced Similarity for User 0:", quantum_sim)
