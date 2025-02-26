# quantumSimulation/utils.py

import json
import os

def save_results(results, file_path):
    """Save simulation results to a JSON file."""
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w') as f:
            json.dump(results, f, indent=4)
        print(f"Results saved to {file_path}")
    except Exception as e:
        print(f"Error saving results: {e}")

def load_results(file_path):
    """Load simulation results from a JSON file."""
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

def log_message(message, log_file='logs/simulation.log'):
    """Log a message to a specified log file."""
    try:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, 'a') as f:
            f.write(f"{message}\n")
        print(f"Logged message: {message}")
    except Exception as e:
        print(f"Error logging message: {e}")

# Example usage
if __name__ == "__main__":
    # Example of saving and loading results
    sample_results = {"result": "quantum state", "counts": {"0": 500, "1": 300}}
    save_results(sample_results, 'results/sample_simulation_results.json')
    loaded_results = load_results('results/sample_simulation_results.json')
    print(loaded_results)

    # Example of logging a message
    log_message("This is a test log message for quantum simulation.")
