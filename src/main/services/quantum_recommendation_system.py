# src/main/services/quantum_recommendation_system.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from qiskit import Aer
from qiskit.circuit.library import RealAmplitudes
from qiskit_machine_learning.algorithms import VQC
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split, GridSearchCV

class QuantumRecommendationSystem:
    def __init__(self, n_qubits):
        self.n_qubits = n_qubits
        self.backend = Aer.get_backend('aer_simulator')
        self.model = None

    def fit(self, user_item_matrix):
        """Fit the quantum recommendation model."""
        self.user_item_matrix = user_item_matrix
        self.model = VQC(quantum_instance=self.backend, feature_map=RealAmplitudes(num_qubits=self.n_qubits, reps=2))

    def recommend(self, user_index, n_recommendations=5):
        """Recommend items for a given user."""
        user_vector = self.user_item_matrix[user_index].reshape(1, -1)
        similarities = cosine_similarity(user_vector, self.user_item_matrix)
        recommended_indices = np.argsort(similarities[0])[-n_recommendations:][::-1]
        return recommended_indices

    def hyperparameter_tuning(self, user_item_matrix):
        """Perform hyperparameter tuning using GridSearchCV."""
        param_grid = {
            'feature_map': [RealAmplitudes(num_qubits=self.n_qubits, reps=1), RealAmplitudes(num_qubits=self.n_qubits, reps=2)],
            'optimizer': ['SLSQP', 'COBYLA']
        }
        grid_search = GridSearchCV(VQC(quantum_instance=self.backend), param_grid, cv=3)
        grid_search.fit(user_item_matrix)
        self.model = grid_search.best_estimator_
        print("Best parameters found: ", grid_search.best_params_)

    def visualize_recommendations(self, user_index, recommendations):
        """Visualize the recommended items for a user."""
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(recommendations)), recommendations, tick_label=[f'Item {i}' for i in recommendations])
        plt.title(f'Recommended Items for User {user_index}')
        plt.xlabel('Items')
        plt.ylabel('Recommendation Score')
        plt.grid()
        plt.show()

# Example usage
if __name__ == "__main__":
    # Simulated user-item interaction matrix
    np.random.seed(42)
    user_item_matrix = np.random.rand(10, 5)  # 10 users, 5 items

    recommender = QuantumRecommendationSystem(n_qubits=3)
    recommender.fit(user_item_matrix)

    user_index = 0
    recommendations = recommender.recommend(user_index)
    print("Recommended Items for User 0:", recommendations)

    # Visualize the recommendations
    recommender.visualize_recommendations(user_index, recommendations)
