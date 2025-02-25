from sklearn.model_selection import ParameterGrid

def hyperparameter_tuning(param_grid: dict):
    """Perform hyperparameter tuning using grid search."""
    grid = ParameterGrid(param_grid)
    best_score = float('-inf')
    best_params = None

    for params in grid:
        print(f"Training with parameters: {params}")
        # Here you would call your training function and evaluate the model
        # For example:
        # score = train_and_evaluate(params)
        score = 0  # Placeholder for actual score

        if score > best_score:
            best_score = score
            best_params = params

    print(f"Best parameters: {best_params} with score: {best_score}")
    return best_params

# Example usage
if __name__ == "__main__":
    param_grid = {
        'epochs': [5, 10],
        'batch_size': [16, 32],
        'learning_rate': [1e-5, 5e-5]
    }
    best_params = hyperparameter_tuning(param_grid)
