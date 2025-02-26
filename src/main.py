# src/main.py

import argparse
import numpy as np
import logging
from automated_system import AutomatedSystem

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Automated System for Quantum Optimization and AI Decision Making")
    parser.add_argument('--num_qubits', type=int, default=3, help='Number of qubits for quantum optimization')
    parser.add_argument('--layers', type=int, default=2, help='Number of layers for QAOA')
    parser.add_argument('--iterations', type=int, default=100, help='Number of optimization iterations')
    parser.add_argument('--train_data', type=str, help='Path to training data (numpy .npy file)')
    parser.add_argument('--test_data', type=str, help='Path to test data (numpy .npy file)')
    return parser.parse_args()

def load_data(file_path):
    """Load numpy data from a file."""
    try:
        data = np.load(file_path)
        return data
    except Exception as e:
        logging.error(f"Error loading data from {file_path}: {e}")
        return None

def main():
    args = parse_arguments()

    # Initialize the automated system
    automated_system = AutomatedSystem(num_qubits=args.num_qubits)

    # Load training data if provided
    X_train, y_train = None, None
    if args.train_data:
        train_data = load_data(args.train_data)
        if train_data is not None:
            X_train, y_train = train_data[:, :-1], train_data[:, -1]  # Assuming last column is the label

    # Load test data if provided
    X_test = None
    if args.test_data:
        X_test = load_data(args.test_data)

    # Execute the automated system
    automated_system.execute(p=args.layers, iterations=args.iterations, X_train=X_train, y_train=y_train, X_test=X_test)

if __name__ == "__main__":
    main()
