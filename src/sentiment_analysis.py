# src/sentiment_analysis.py

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import joblib

class SentimentAnalyzer:
    def __init__(self):
        self.model = make_pipeline(CountVectorizer(), MultinomialNB())

    def train(self, X, y):
        """Train the sentiment analysis model."""
        self.model.fit(X, y)

    def predict(self, texts):
        """Predict sentiment for given texts."""
        return self.model.predict(texts)

    def save_model(self, filename):
        """Save the trained model to a file."""
        joblib.dump(self.model, filename)

    def load_model(self, filename):
        """Load a trained model from a file."""
        self.model = joblib.load(filename)

# Example usage
if __name__ == "__main__":
    # Sample training data
    X = np.array(["I love this!", "This is terrible.", "I feel great about this.", "I am not happy."])
    y = np.array([1, 0, 1, 0])  # 1 for positive, 0 for negative

    analyzer = SentimentAnalyzer()
    analyzer.train(X, y)

    # Sample texts for prediction
    texts = np.array(["I am so happy!", "This is the worst!"])
    predictions = analyzer.predict(texts)
    print(f"Predictions: {predictions}")
