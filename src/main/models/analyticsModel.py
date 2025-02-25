# analyticsModel.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalyticsModel:
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = None
        self.model = None

    def load_data(self):
        """Load the dataset from the specified path."""
        logger.info("Loading data...")
        self.data = pd.read_csv(self.data_path)
        logger.info(f"Data loaded successfully with shape: {self.data.shape}")

    def preprocess_data(self):
        """Preprocess the data for analysis."""
        logger.info("Preprocessing data...")
        # Example preprocessing steps
        self.data.dropna(inplace=True)  # Remove missing values
        self.data = pd.get_dummies(self.data)  # Convert categorical variables to dummy variables
        logger.info("Data preprocessing completed.")

    def exploratory_data_analysis(self):
        """Perform exploratory data analysis (EDA)."""
        logger.info("Performing exploratory data analysis...")
        # Summary statistics
        logger.info(self.data.describe())

        # Visualizations
        plt.figure(figsize=(10, 6))
        sns.histplot(self.data['target'], bins=30, kde=True)
        plt.title('Distribution of Target Variable')
        plt.xlabel('Target')
        plt.ylabel('Frequency')
        plt.show()

        # Correlation heatmap
        plt.figure(figsize=(12, 8))
        sns.heatmap(self.data.corr(), annot=True, fmt=".2f", cmap='coolwarm')
        plt.title('Correlation Heatmap')
        plt.show()

    def train_model(self, target_column):
        """Train a predictive model."""
        logger.info("Training model...")
        X = self.data.drop(target_column, axis=1)
        y = self.data[target_column]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.model = LinearRegression()
        self.model.fit(X_train, y_train)

        # Evaluate the model
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        logger.info(f"Model trained successfully. MSE: {mse:.2f}, R^2: {r2:.2f}")

    def visualize_predictions(self, X_test, y_test):
        """Visualize the model predictions against actual values."""
        logger.info("Visualizing predictions...")
        y_pred = self.model.predict(X_test)

        plt.figure(figsize=(10, 6))
        plt.scatter(y_test, y_pred)
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
        plt.xlabel('Actual Values')
        plt.ylabel('Predicted Values')
        plt.title('Actual vs Predicted Values')
        plt.show()

    def save_model(self, model_path='analytics_model.pkl'):
        """Save the trained model to disk."""
        import joblib
        joblib.dump(self.model, model_path)
        logger.info(f"Model saved to {model_path}")

    def load_model(self, model_path='analytics_model.pkl'):
        """Load a trained model from disk."""
        import joblib
        self.model = joblib.load(model_path)
        logger.info(f"Model loaded from {model_path}")

if __name__ == "__main__":
    # Example usage
    data_path = 'data.csv'  # Path to your dataset
    analytics_model = AnalyticsModel(data_path)
    analytics_model.load_data()
    analytics_model.preprocess_data()
    analytics_model.exploratory_data_analysis()
    analytics_model.train_model(target_column='target')  # Replace 'target' with your actual target column name

    # Visualize predictions
    X = analytics_model.data.drop('target', axis=1)
    y = analytics_model.data['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    analytics_model.visualize_predictions(X_test, y_test)

    # Save the model
    analytics_model.save_model()
