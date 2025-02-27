# src/main/services/quantum_portfolio_optimization.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from qiskit import Aer
from qiskit.circuit.library import QAOA
from qiskit.primitives import Sampler
from qiskit.algorithms import NumPyMinimumEigensolver
from scipy.optimize import minimize

class QuantumPortfolioOptimization:
    def __init__(self, returns):
        self.returns = returns
        self.backend = Aer.get_backend('aer_simulator')

    def objective_function(self, weights):
        """Objective function to minimize (negative Sharpe ratio)."""
        portfolio_return = np.dot(weights, self.returns.mean())
        portfolio_std_dev = np.sqrt(np.dot(weights.T, np.dot(np.cov(self.returns.T), weights)))
        sharpe_ratio = portfolio_return / portfolio_std_dev
        return -sharpe_ratio  # Minimize negative Sharpe ratio

    def risk_metrics(self, weights):
        """Calculate risk metrics for the portfolio."""
        portfolio_return = np.dot(weights, self.returns.mean())
        portfolio_std_dev = np.sqrt(np.dot(weights.T, np.dot(np.cov(self.returns.T), weights)))
        var = -np.percentile(np.dot(self.returns, weights), 5)  # Value at Risk at 95% confidence
        cvar = -np.mean(np.dot(self.returns, weights)[np.dot(self.returns, weights) <= -var])  # Conditional VaR
        return portfolio_return, portfolio_std_dev, var, cvar

    def optimize_portfolio(self):
        """Optimize the portfolio using QAOA."""
        num_assets = len(self.returns.columns)
        initial_weights = np.ones(num_assets) / num_assets  # Equal distribution
        bounds = tuple((0, 1) for _ in range(num_assets))
        constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}  # Weights must sum to 1

        # Use classical optimization to find the optimal weights
        result = minimize(self.objective_function, initial_weights, bounds=bounds, constraints=constraints)
        optimal_weights = result.x

        # Calculate risk metrics for the optimal portfolio
        portfolio_return, portfolio_std_dev, var, cvar = self.risk_metrics(optimal_weights)
        print(f"Optimal Weights: {optimal_weights}")
        print(f"Expected Return: {portfolio_return:.4f}, Risk (Std Dev): {portfolio_std_dev:.4f}, VaR: {var:.4f}, CVaR: {cvar:.4f}")

        return optimal_weights

    def visualize_portfolio(self, optimal_weights):
        """Visualize the optimized portfolio allocation."""
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(optimal_weights)), optimal_weights, tick_label=self.returns.columns)
        plt.title('Optimized Portfolio Allocation')
        plt.xlabel('Assets')
        plt.ylabel('Weights')
        plt.grid()
        plt.show()

# Example usage
if __name__ == "__main__":
    # Simulated returns for 3 assets
    np.random.seed(42)
    returns = np.random.normal(0.01, 0.02, (1000, 3))
    returns_df = pd.DataFrame(returns, columns=['Asset 1', 'Asset 2', 'Asset 3'])

    optimizer = QuantumPortfolioOptimization(returns_df)
    optimal_weights = optimizer.optimize_portfolio()
    optimizer.visualize_portfolio(optimal_weights)
