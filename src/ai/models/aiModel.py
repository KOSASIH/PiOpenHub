import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib

class AIModel:
    def __init__(self, data):
        self.data = data
        self.model = None

    def preprocess_data(self):
        # Remove missing values
        self.data.dropna(inplace=True)
        # Separate features and target
        X = self.data.drop('target', axis=1)  # Replace 'target' with your actual target column name
        y = self.data['target']  # Replace 'target' with your actual target column name
        return train_test_split(X, y, test_size=0.2, random_state=42)

    def create_pipeline(self):
        # Create a machine learning pipeline
        pipeline = Pipeline([
            ('scaler', StandardScaler()),  # Feature scaling
            ('classifier', RandomForestClassifier())  # Random Forest Classifier
        ])
        return pipeline

    def tune_hyperparameters(self, X_train, y_train):
        # Define hyperparameter grid
        param_grid = {
            'classifier__n_estimators': [50, 100, 200],
            'classifier__max_depth': [None, 10, 20, 30],
            'classifier__min_samples_split': [2, 5, 10]
        }
        grid_search = GridSearchCV(self.create_pipeline(), param_grid, cv=5, n_jobs=-1, verbose=1)
        grid_search.fit(X_train, y_train)
        return grid_search.best_estimator_

    def train_model(self):
        X_train, X_test, y_train, y_test = self.preprocess_data()
        self.model = self.tune_hyperparameters(X_train, y_train)
        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f'Model accuracy: {accuracy:.2f}')
        print(classification_report(y_test, predictions))

    def save_model(self, filename='ai_model.pkl'):
        # Save the trained model to a file
        joblib.dump(self.model, filename)
        print(f'Model saved to {filename}')

    def load_model(self, filename='ai_model.pkl'):
        # Load a trained model from a file
        self.model = joblib.load(filename)
        print(f'Model loaded from {filename}')

    def predict(self, new_data):
        if self.model is None:
            raise Exception("Model is not trained or loaded. Please train or load a model first.")
        return self.model.predict(new_data)

# Example usage
if __name__ == "__main__":
    # Import data
    data = pd.read_csv('data.csv')  # Replace with the path to your dataset
    ai_model = AIModel(data)
    ai_model.train_model()
    ai_model.save_model()

    # Example prediction with new data
    new_data = np.array([[5.1, 3.5, 1.4, 0.2]])  # Replace with appropriate feature values
    prediction = ai_model.predict(new_data)
    print(f'Prediction for new data: {prediction}')

    # Load the model and make a prediction
    ai_model.load_model()
    prediction = ai_model.predict(new_data)
    print(f'Prediction for new data after loading model: {prediction}')
