# src/ai_decision_maker.py

import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report
import joblib

class AIDecisionMaker:
    def __init__(self):
        self.model = None

    def train(self, X, y):
        """Train the decision-making model using an ensemble of classifiers."""
        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Define the models to be used
        models = {
            'RandomForest': RandomForestClassifier(),
            'GradientBoosting': GradientBoostingClassifier()
        }

        best_model = None
        best_accuracy = 0

        # Train and evaluate each model
        for name, model in models.items():
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)
            accuracy = accuracy_score(y_test, predictions)
            print(f"{name} Accuracy: {accuracy:.2f}")
            print(classification_report(y_test, predictions))

            # Save the best model based on accuracy
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_model = model

        self.model = best_model
        print(f"Best model: {best_model.__class__.__name__} with accuracy: {best_accuracy:.2f}")

    def predict(self, X):
        """Make predictions using the trained model."""
        if self.model is None:
            raise Exception("Model has not been trained yet.")
        return self.model.predict(X)

    def save_model(self, filename):
        """Save the trained model to a file."""
        if self.model is None:
            raise Exception("Model has not been trained yet.")
        joblib.dump(self.model, filename)
        print(f"Model saved to {filename}")

    def load_model(self, filename):
        """Load a trained model from a file."""
        self.model = joblib.load(filename)
        print(f"Model loaded from {filename}")

# Example usage
if __name__ == "__main__":
    # Sample training data (features and labels)
    X = np.array([[0, 0], [1, 1], [1, 0], [0, 1], [1, 1], [0, 0]])
    y = np.array([0, 1, 1, 0, 1, 0])  # Example labels

    decision_maker = AIDecisionMaker()
    decision_maker.train(X, y)

    # Sample input for prediction
    X_test = np.array([[0, 1], [1, 0], [1, 1]])
    predictions = decision_maker.predict(X_test)
    print(f"Predictions: {predictions}")

    # Save the trained model
    decision_maker.save_model("best_model.pkl")

    # Load the model
    decision_maker.load_model("best_model.pkl")
    loaded_predictions = decision_maker.predict(X_test)
    print(f"Loaded model predictions: {loaded_predictions}")
