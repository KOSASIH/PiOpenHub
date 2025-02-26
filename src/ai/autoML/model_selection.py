# autoML/model_selection.py

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from .config import Config
import joblib

def train_model(X_train, y_train, model_type='random_forest'):
    """Train a model based on the specified type."""
    if model_type == 'random_forest':
        model = RandomForestClassifier(random_state=Config.RANDOM_STATE)
    elif model_type == 'logistic_regression':
        model = LogisticRegression(max_iter=200)
    elif model_type == 'svm':
        model = SVC()
    else:
        raise ValueError("Unsupported model type. Choose from 'random_forest', 'logistic_regression', or 'svm'.")

    model.fit(X_train, y_train)
    print(f"{model_type} model trained successfully.")
    return model

def select_best_model(X_train, y_train):
    """Select the best model based on accuracy."""
    models = ['random_forest', 'logistic_regression', 'svm']
    best_model = None
    best_accuracy = 0

    for model_type in models:
        model = train_model(X_train, y_train, model_type)
        y_pred = model.predict(X_train)
        accuracy = accuracy_score(y_train, y_pred)
        print(f"{model_type} accuracy: {accuracy:.4f}")

        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_model = model

    print(f"Best model: {best_model.__class__.__name__} with accuracy: {best_accuracy:.4f}")
    return best_model

def save_model(model):
    """Save the trained model to a file."""
    joblib.dump(model, Config.MODEL_SAVE_PATH)
    print(f"Model saved to {Config.MODEL_SAVE_PATH}")
