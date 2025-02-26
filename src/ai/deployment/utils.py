# ai/deployment/utils.py

import joblib

def load_model(model_path):
    """Load a model from the specified path."""
    try:
        model = joblib.load(model_path)
        print(f"Model loaded from {model_path}")
        return model
    except FileNotFoundError:
        print(f"Model file not found at {model_path}. Please check the path.")
        return None
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def save_model(model, model_path):
    """Save a model to the specified path."""
    try:
        joblib.dump(model, model_path)
        print(f"Model saved to {model_path}")
    except Exception as e:
        print(f"Error saving model: {e}")

def validate_features(features, expected_length):
    """Validate the input features."""
    if not isinstance(features, list):
        raise ValueError("Features should be a list.")
    if len(features) != expected_length:
        raise ValueError(f"Expected {expected_length} features, but got {len(features)}.")

# Example usage
if __name__ == "__main__":
    # Example model path
    model_path = 'models/my_model.pkl'
    
    # Load a model
    model = load_model(model_path)
    
    # Save a model (assuming `model` is defined)
    # save_model(model, model_path)

    # Validate features
    try:
        validate_features([5.1, 3.5, 1.4, 0.2], 4)
        print("Features are valid.")
    except ValueError as e:
        print(f"Feature validation error: {e}")
