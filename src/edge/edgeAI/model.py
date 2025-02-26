# edgeAI/model.py

import joblib
import numpy as np
from .config import Config

def load_model():
    """Load the machine learning model from the specified path."""
    try:
        model = joblib.load(Config.MODEL_PATH)
        print(f"Model loaded successfully from {Config.MODEL_PATH}")
        return model
    except FileNotFoundError:
        raise FileNotFoundError(f"Model file not found at {Config.MODEL_PATH}. Please check the path.")
    except Exception as e:
        raise Exception(f"Error loading model: {e}")

def run_inference(model, data):
    """Run inference on the input data using the loaded model."""
    try:
        # Ensure data is in the correct format (e.g., 2D array)
        if isinstance(data, np.ndarray):
            if data.ndim == 1:
                data = data.reshape(1, -1)  # Reshape for single sample
        elif isinstance(data, list):
            data = np.array(data).reshape(1, -1)  # Convert list to array and reshape
        else:
            raise ValueError("Input data must be a numpy array or a list.")

        predictions = model.predict(data)
        print("Inference completed successfully.")
        return predictions
    except Exception as e:
        raise Exception(f"Error during inference: {e}")
