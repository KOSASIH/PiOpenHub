import jwt
import datetime
from functools import wraps
from flask import request, jsonify, current_app
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Secret key for JWT encoding and decoding
SECRET_KEY = current_app.config.get('SECRET_KEY', 'your_secret_key')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check if token is passed in the headers
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        # If no token, return an error
        if not token:
            logger.warning("Token is missing.")
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            # Decode the token
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = data['user_id']
            # Optionally, you can fetch user details from the database here
            # user = User.query.filter_by(id=current_user).first()
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired.")
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            logger.warning("Invalid token.")
            return jsonify({'message': 'Invalid token!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

def generate_token(user_id, expiration_minutes=30):
    """Generate a new JWT token."""
    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration_minutes)
    token = jwt.encode({'user_id': user_id, 'exp': expiration}, SECRET_KEY, algorithm="HS256")
    return token

def role_required(role):
    """Decorator to check user role."""
    def decorator(f):
        @wraps(f)
        @token_required
        def decorated(current_user, *args, **kwargs):
            # Here you would typically fetch the user from the database
            # user = User.query.filter_by(id=current_user).first()
            user_role = 'user'  # Replace with actual user role fetching logic

            if user_role != role:
                logger.warning(f"User {current_user} does not have the required role: {role}.")
                return jsonify({'message': 'You do not have permission to access this resource.'}), 403

            return f(current_user, *args, **kwargs)

        return decorated
    return decorator

# Example usage of the middleware
# @app.route('/protected', methods=['GET'])
# @token_required
# def protected_route(current_user):
#     return jsonify({'message': f'Welcome user {current_user}!'})

# @app.route('/admin', methods=['GET'])
# @role_required('admin')
# def admin_route(current_user):
#     return jsonify({'message': 'Welcome to the admin panel!'})
