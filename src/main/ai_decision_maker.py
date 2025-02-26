# src/main/ai_decision_maker.py

from sklearn.tree import DecisionTreeClassifier
import numpy as np

class AIDecisionMaker:
    def __init__(self):
        self.model = DecisionTreeClassifier()

    def train(self, X, y):
        """Train the decision tree model."""
        self.model.fit(X, y)

    def predict(self, X):
        """Make predictions using the trained model."""
        return self.model.predict(X)

# Example usage
if __name__ == "__main__":
    # Sample training data (features and labels)
    X_train = np.array([[0, 0], [1, 1], [1, 0], [0, 1]])
    y_train = np.array([0, 1, 1, 0])  # Example labels

    decision_maker = AIDecisionMaker()
    decision_maker.train(X_train, y_train)

    # Sample input for prediction
    X_test = np.array([[0, 1], [1, 1]])
    predictions = decision_maker.predict(X_test)
    print(f"Predictions: {predictions}")
