from sklearn.metrics import accuracy_score, f1_score

def calculate_accuracy(y_true, y_pred) -> float:
    """Calculate accuracy of predictions."""
    return accuracy_score(y_true, y_pred)

def calculate_f1_score(y_true, y_pred) -> float:
    """Calculate F1 score of predictions."""
    return f1_score(y_true, y_pred, average='weighted')
