import os
import pytest
from flask import Flask
from flask.testing import FlaskClient
from myapp import create_app  # Assuming your Flask app factory is in myapp.py
from myapp.errorHandler import APIException, NotFoundException
from myapp.dataFormatter import DataFormatter
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

def test_api_response_format(client: FlaskClient):
    """Test the API response format."""
    response = client.get('/example')  # Assuming this route raises a NotFoundException
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data['status'] == 'error'
    assert json_data['message'] == 'Resource not found.'
    assert json_data['code'] == 404

def test_ml_model_prediction(client: FlaskClient, ml_service: MLModelService):
    """Test the ML model prediction endpoint."""
    test_data = [[5.1, 3.5, 1.4, 0.2]]  # Example input for prediction
    response = client.post('/predict', json={'data': test_data})
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'success'
    assert 'predictions' in json_data

def test_data_formatting(client: FlaskClient):
    """Test the data formatting utility."""
    example_data = {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com"
    }
    formatted_response = DataFormatter.format_response(example_data, message="User retrieved successfully.")
    assert formatted_response['status'] == 'success'
    assert formatted_response['message'] == "User retrieved successfully."
    assert formatted_response['data'] == example_data

def test_error_handling(client: FlaskClient):
    """Test the error handling for unauthorized access."""
    response = client.get('/unauthorized')  # Assuming this route raises an UnauthorizedException
    assert response.status_code == 401
    json_data = response.get_json()
    assert json_data['status'] == 'error'
    assert json_data['message'] == 'Unauthorized access.'
    assert json_data['code'] == 401

def test_integration(client: FlaskClient):
    """Test the integration of multiple components."""
    # Simulate a full workflow: Train model, load it, and make a prediction
    ml_service = MLModelService()
    ml_service.train_model()
    ml_service.load_model()

    test_data = [[5.1, 3.5, 1.4, 0.2]]  # Example input for prediction
    response = client.post('/predict', json={'data': test_data})
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'success'
    assert 'predictions' in json_data

if __name__ == '__main__':
    pytest.main()
