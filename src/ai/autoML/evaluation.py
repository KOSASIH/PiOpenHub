# autoML/evaluation.py

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
from .config import Config

def evaluate_model(model, X_test, y_test):
    """Evaluate the model on the test set and print evaluation metrics."""
    y_pred = model.predict(X_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.4f}")

    # Print classification report
    report = classification_report(y_test, y_pred)
    print("Classification Report:")
    print(report)

    # Print confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print("Confusion Matrix:")
    print(cm)

def save_model(model):
    """Save the trained model to a file."""
    joblib.dump(model, Config.MODEL_SAVE_PATH)
    print(f"Model saved to {Config.MODEL_SAVE_PATH}")

# Example usage
if __name__ == "__main__":
    # This section can be used for testing the evaluation functions
    from autoML.data_preprocessing import load_data, preprocess_data
    from autoML.model_selection import train_model

    # Load and preprocess data
    data = load_data()
    X_train, X_test, y_train, y_test = preprocess_data(data)

    # Train a model (example with Random Forest)
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(random_state=Config.RANDOM_STATE)
    model.fit(X_train, y_train)

    # Evaluate the model
    evaluate_model(model, X_test, y_test)
