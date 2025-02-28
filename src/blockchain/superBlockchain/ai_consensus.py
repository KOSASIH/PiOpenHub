import numpy as np
from sklearn.linear_model import LinearRegression
import random

class AdaptiveConsensus:
    def __init__(self):
        self.network_conditions = []  # List to store network conditions
        self.model = LinearRegression()  # Machine learning model for prediction
        self.is_trained = False  # Flag to check if the model is trained

    def update_network_conditions(self, condition):
        """Update the list of network conditions with a new condition."""
        self.network_conditions.append(condition)

    def train_model(self):
        """Train the machine learning model based on historical network conditions."""
        if len(self.network_conditions) < 2:
            print("Not enough data to train the model.")
            return
        
        # Prepare data for training
        X = np.array(range(len(self.network_conditions))).reshape(-1, 1)  # Time steps
        y = np.array(self.network_conditions)  # Network conditions
        self.model.fit(X, y)
        self.is_trained = True
        print("Model trained successfully.")

    def predict_network_condition(self):
        """Predict the next network condition using the trained model."""
        if not self.is_trained:
            print("Model is not trained yet.")
            return None
        
        next_time_step = np.array([[len(self.network_conditions)]])  # Next time step
        predicted_condition = self.model.predict(next_time_step)
        return predicted_condition[0]

    def decide_consensus(self):
        """Decide whether consensus is reached based on the predicted network condition."""
        if not self.is_trained:
            print("Model is not trained yet.")
            return "No consensus"

        predicted_condition = self.predict_network_condition()
        print(f"Predicted Network Condition: {predicted_condition}")

        # Define a threshold for consensus
        threshold = 0.5
        return "Consensus reached" if predicted_condition > threshold else "Consensus not reached"

# Example usage
if __name__ == "__main__":
    consensus = AdaptiveConsensus()
    
    # Simulate updating network conditions
    for _ in range(10):
        condition = random.uniform(0, 1)  # Random network condition between 0 and 1
        consensus.update_network_conditions(condition)
        print(f"Updated Network Condition: {condition}")

    # Train the model
    consensus.train_model()

    # Decide consensus
    result = consensus.decide_consensus()
    print(result)
