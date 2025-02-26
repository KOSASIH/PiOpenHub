# edgeAI/inference.py

from .config import Config
from .model import load_model, run_inference
from .data_preprocessing import preprocess_data
from .utils import save_results
import pandas as pd

def perform_inference(input_data):
    """Perform inference on the input data."""
    # Load the model
    model = load_model()
    
    # Preprocess the input data
    processed_data = preprocess_data(input_data)
    
    # Run inference
    predictions = run_inference(model, processed_data)
    
    # Save the results
    save_results(predictions.tolist(), Config.RESULTS_PATH)

# Example usage
if __name__ == "__main__":
    # Example input data as a DataFrame
    input_data = pd.DataFrame({
        'feature1': [1.0, 2.0, 3.0],
        'feature2': [4.0, 5.0, 6.0]
    })

    perform_inference(input_data)
