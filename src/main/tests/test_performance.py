import time
import pytest
from flask import Flask
from flask.testing import FlaskClient
from myapp import create_app  # Assuming your Flask app factory is in myapp.py
from myapp.mlOpsService import MLModelService

@pytest.fixture
def app() -> Flask:
    """Create a Flask application for testing."""
    app = create_app()
    app.config['TESTING'] = True
    yield app

@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """Create a test client for the app."""
    return app.test_client()

@pytest.fixture
def ml_service() -> MLModelService:
    """Create an instance of the MLModelService for testing."""
    service = MLModelService()
    service.train_model()  # Train the model for testing
    service.load_model()   # Load the model for predictions
    return service

def test_prediction_performance(client: FlaskClient, ml_service: MLModelService):
    """Test the performance of the prediction endpoint."""
    test_data = [[5.1, 3.5, 1.4, 0.2]]  # Example input for prediction

    start_time = time.time()
    response = client.post('/predict', json={'data': test_data})
    end_time = time.time()

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'success'
    assert 'predictions' in json_data

    # Measure performance
    duration = end_time - start_time
    print(f"Prediction endpoint response time: {duration:.4f} seconds")
    assert duration < 0.5  # Assert that the response time is less than 500ms

def test_data_formatting_performance(client: FlaskClient):
    """Test the performance of the data formatting utility."""
    example_data = {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com"
    }

    start_time = time.time()
    formatted_response = DataFormatter.format_response(example_data, message="User retrieved successfully.")
    end_time = time.time()

    assert formatted_response['status'] == 'success'
    assert formatted_response['message'] == "User retrieved successfully."
    assert formatted_response['data'] == example_data

    # Measure performance
    duration = end_time - start_time
    print(f"Data formatting response time: {duration:.4f} seconds")
    assert duration < 0.1  # Assert that the response time is less than 100ms

def test_model_training_performance(ml_service: MLModelService):
    """Test the performance of the model training process."""
    start_time = time.time()
    ml_service.train_model()
    end_time = time.time()

    # Measure performance
    duration = end_time - start_time
    print(f"Model training time: {duration:.4f} seconds")
    assert duration < 5.0  # Assert that the training time is less than 5 seconds

if __name__ == '__main__':
    pytest.main()
