# autoML/hyperparameter_tuning.py

from sklearn.model_selection import GridSearchCV
from .model_selection import train_model
from .config import Config

def tune_hyperparameters(X_train, y_train):
    """Tune hyperparameters for the Random Forest model using Grid Search."""
    # Define the parameter grid for Random Forest
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10]
    }

    # Initialize the model
    model = train_model(X_train, y_train, model_type='random_forest')

    # Set up Grid Search
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, scoring='accuracy', n_jobs=-1)
    
    # Fit Grid Search
    grid_search.fit(X_train, y_train)

    # Output the best parameters and best score
    print("Best Hyperparameters:", grid_search.best_params_)
    print("Best Cross-Validation Score:", grid_search.best_score_)

    # Return the best estimator
    return grid_search.best_estimator_

# Example usage
if __name__ == "__main__":
    from autoML.data_preprocessing import load_data, preprocess_data

    # Load and preprocess data
    data = load_data()
    X_train, X_test, y_train, y_test = preprocess_data(data)

    # Tune hyperparameters
    best_model = tune_hyperparameters(X_train, y_train)
