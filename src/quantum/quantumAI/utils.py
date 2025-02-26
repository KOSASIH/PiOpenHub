# quantumAI/utils.py

import json
import os

def save_results(results, file_path):
    """Save AI results to a JSON file."""
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w') as f:
            json.dump(results, f, indent=4)
        print(f"Results saved to {file_path}")
    except Exception as e:
        print(f"Error saving results: {e}")

def load_results(file_path):
    """Load AI results from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            results = json.load(f)
        print(f"Results loaded from {file_path}")
        return results
    except FileNotFoundError:
        print(f"File not found at {file_path}. Please check the path.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file at {file_path}.")
        return None
    except Exception as e:
        print(f"Error loading results: {e}")
        return None
