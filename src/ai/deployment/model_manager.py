# ai/deployment/model_manager.py

import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from .config import Config

class ModelManager:
    """Class to manage AI model training, saving, and loading."""

    def __init__(self):
        self.model = None

    def train_model(self):
        """Train a Random Forest model on the Iris dataset."""
        print("Loading Iris dataset...")
        data = load_iris()
        X, y = data.data, data.target
        
        print("Training the model...")
        self.model = RandomForestClassifier()
        self.model.fit(X, y)
        print("Model trained successfully.")

    def save_model(self):
        """Save the trained model to a file."""
        if self.model is not None:
            joblib.dump(self.model, Config.MODEL_PATH)
            print(f"Model saved to {Config.MODEL_PATH}")
        else:
            print("No model to save.")

    def load_model(self):
        """Load the model from a file."""
        try:
            self.model = joblib.load(Config.MODEL_PATH)
            print("Model loaded successfully.")
        except FileNotFoundError:
            print(f"Model file not found at {Config.MODEL_PATH}. Please train the model first.")
        except Exception as e:
            print(f"Error loading model: {e}")

# Example usage
if __name__ == "__main__":
    model_manager = ModelManager()
    
    # Train the model
    model_manager.train_model()
    
    # Save the model
    model_manager.save_model()
    
    # Load the model
    model_manager.load_model()
