# src/edge/federated_learning.py

import numpy as np
import logging
from sklearn.base import clone
from sklearn.metrics import accuracy_score
from collections import defaultdict

class FederatedLearning:
    """
    Implementation of Federated Learning for edge devices.
    
    This class simulates a federated learning environment where multiple
    edge devices train models locally and aggregate their parameters.
    """
    
    def __init__(self, base_model, num_clients=5):
        """
        Initialize the Federated Learning system.
        
        Args:
            base_model: The base model to be used by all clients (must support fit and predict)
            num_clients (int): Number of simulated client devices
        """
        self.base_model = base_model
        self.num_clients = num_clients
        self.client_models = [clone(base_model) for _ in range(num_clients)]
        self.global_model = clone(base_model)
        self.logger = logging.getLogger(__name__)
        
    def distribute_data(self, X, y, method='iid'):
        """
        Distribute data among clients.
        
        Args:
            X (numpy.ndarray): Features
            y (numpy.ndarray): Labels
            method (str): Data distribution method ('iid' or 'non-iid')
            
        Returns:
            list: List of (X, y) tuples for each client
        """
        n_samples = len(X)
        client_data = []
        
        if method == 'iid':
            # IID distribution: randomly shuffle and distribute
            indices = np.random.permutation(n_samples)
            client_size = n_samples // self.num_clients
            
            for i in range(self.num_clients):
                start_idx = i * client_size
                end_idx = (i + 1) * client_size if i < self.num_clients - 1 else n_samples
                client_indices = indices[start_idx:end_idx]
                client_data.append((X[client_indices], y[client_indices]))
                
        elif method == 'non-iid':
            # Non-IID distribution: distribute by class
            classes = np.unique(y)
            class_indices = {c: np.where(y == c)[0] for c in classes}
            
            # Distribute classes unevenly among clients
            client_classes = {}
            for i in range(self.num_clients):
                # Each client gets a subset of classes
                n_classes = max(1, len(classes) // 2)
                client_classes[i] = np.random.choice(classes, size=n_classes, replace=False)
            
            for i in range(self.num_clients):
                client_indices = []
                for c in client_classes[i]:
                    # Get indices for this class
                    class_idx = class_indices[c]
                    # Take a portion of the class data
                    n_samples_class = len(class_idx) // sum([1 for j in range(self.num_clients) if c in client_classes[j]])
                    client_indices.extend(np.random.choice(class_idx, size=n_samples_class, replace=False))
                
                client_data.append((X[client_indices], y[client_indices]))
        else:
            raise ValueError(f"Unknown data distribution method: {method}")
            
        return client_data
        
    def train_round(self, client_data, local_epochs=1):
        """
        Perform one round of federated training.
        
        Args:
            client_data (list): List of (X, y) tuples for each client
            local_epochs (int): Number of local training epochs
            
        Returns:
            dict: Training metrics
        """
        client_metrics = defaultdict(list)
        
        # Train each client model locally
        for i, (X, y) in enumerate(client_data):
            self.logger.info(f"Training client {i+1}/{self.num_clients}")
            
            # Train for multiple local epochs
            for epoch in range(local_epochs):
                self.client_models[i].fit(X, y)
            
            # Evaluate the model
            y_pred = self.client_models[i].predict(X)
            accuracy = accuracy_score(y, y_pred)
            client_metrics['accuracy'].append(accuracy)
            
        # Aggregate model parameters (simplified for demonstration)
        self._aggregate_models()
        
        return dict(client_metrics)
        
    def _aggregate_models(self):
        """
        Aggregate client models into the global model.
        This is a simplified implementation and would need to be adapted
        based on the specific model type being used.
        """
        # This is a placeholder for model aggregation
        # In a real implementation, this would average model parameters
        # For now, we'll just use the first client's model as the global model
        self.global_model = clone(self.client_models[0])
        
        # In a real implementation with PyTorch or TensorFlow:
        # 1. Extract model weights from each client
        # 2. Average the weights
        # 3. Update the global model with the averaged weights
        # 4. Distribute the global model back to clients
        
    def evaluate_global_model(self, X_test, y_test):
        """
        Evaluate the global model on test data.
        
        Args:
            X_test (numpy.ndarray): Test features
            y_test (numpy.ndarray): Test labels
            
        Returns:
            float: Accuracy of the global model
        """
        y_pred = self.global_model.predict(X_test)
        return accuracy_score(y_test, y_pred)
        
    def run_simulation(self, X, y, X_test, y_test, rounds=5, local_epochs=1, data_distribution='iid'):
        """
        Run a complete federated learning simulation.
        
        Args:
            X (numpy.ndarray): Training features
            y (numpy.ndarray): Training labels
            X_test (numpy.ndarray): Test features
            y_test (numpy.ndarray): Test labels
            rounds (int): Number of federated rounds
            local_epochs (int): Number of local training epochs
            data_distribution (str): Data distribution method
            
        Returns:
            dict: Simulation results
        """
        results = {
            'round_metrics': [],
            'global_accuracy': []
        }
        
        # Distribute data among clients
        client_data = self.distribute_data(X, y, method=data_distribution)
        
        # Run federated learning rounds
        for r in range(rounds):
            self.logger.info(f"Starting round {r+1}/{rounds}")
            
            # Train one round
            metrics = self.train_round(client_data, local_epochs)
            results['round_metrics'].append(metrics)
            
            # Evaluate global model
            global_accuracy = self.evaluate_global_model(X_test, y_test)
            results['global_accuracy'].append(global_accuracy)
            
            self.logger.info(f"Round {r+1} completed. Global model accuracy: {global_accuracy:.4f}")
            
        return results

# Example usage
if __name__ == "__main__":
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.datasets import make_classification
    from sklearn.model_selection import train_test_split
    
    # Generate synthetic data
    X, y = make_classification(n_samples=1000, n_features=20, n_classes=2, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create base model
    base_model = RandomForestClassifier(n_estimators=10, random_state=42)
    
    # Initialize federated learning
    fed_learning = FederatedLearning(base_model, num_clients=5)
    
    # Run simulation
    results = fed_learning.run_simulation(
        X_train, y_train, X_test, y_test,
        rounds=3, local_epochs=1, data_distribution='iid'
    )
    
    print(f"Final global model accuracy: {results['global_accuracy'][-1]:.4f}")