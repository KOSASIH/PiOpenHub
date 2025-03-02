from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os

# Import custom utilities
from utils.logger import setup_logger
from utils.errorHandler import handle_error
from routes.userRoutes import user_routes
from routes.transactionRoutes import transaction_routes
from config import Config

# Initialize the Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS for all routes
CORS(app)

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Set up logging
logger = setup_logger('app_logger', 'app.log')

# Register routes
app.register_blueprint(user_routes)
app.register_blueprint(transaction_routes)

@app.route('/')
def home():
    return jsonify(message="Welcome to Pi Open Hub!"), 200

# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify(message="Resource not found"), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Server Error: {error}")
    return handle_error(error)

# JWT token verification callback
@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify(message="Missing or invalid token"), 401

@jwt.expired_token_loader
def expired_token_response(callback):
    return jsonify(message="Token has expired"), 401

@jwt.invalid_token_loader
def invalid_token_response(callback):
    return jsonify(message="Invalid token"), 401

if __name__ == '__main__':
    # Use environment variables for sensitive information
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=os.environ.get('DEBUG', 'True') == 'True')
