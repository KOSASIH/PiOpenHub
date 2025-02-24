from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler
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
if not app.debug:
    handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)

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
    app.logger.error(f"Server Error: {error}")
    return jsonify(message="Internal server error"), 500

# JWT token verification callback
@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify(message="Missing or invalid token"), 401

@jwt.expired_token_loader
def expired_token_response(callback):
    return jsonify(message="Token has expired"), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
