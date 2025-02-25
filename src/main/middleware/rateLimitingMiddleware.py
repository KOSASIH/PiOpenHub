# rateLimitingMiddleware.py

from flask import request, jsonify
import time
from collections import defaultdict

# Rate limiting configuration
RATE_LIMIT = 5  # Maximum number of requests
TIME_WINDOW = 60  # Time window in seconds

# In-memory store for tracking requests
request_counts = defaultdict(list)

def rate_limiting_middleware(app):
    """Rate limiting middleware to limit the number of requests."""
    
    @app.before_request
    def limit_requests():
        """Limit the number of requests from a client."""
        client_ip = request.remote_addr  # Get the client's IP address
        current_time = time.time()

        # Clean up old request timestamps
        request_counts[client_ip] = [timestamp for timestamp in request_counts[client_ip] if current_time - timestamp < TIME_WINDOW]

        # Check if the client has exceeded the rate limit
        if len(request_counts[client_ip]) >= RATE_LIMIT:
            return jsonify({"error": "Too many requests. Please try again later."}), 429

        # Record the current request timestamp
        request_counts[client_ip].append(current_time)

# Example of how to use the middleware in your main application
if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)

    # Register the rate limiting middleware
    rate_limiting_middleware(app)

    @app.route('/example', methods=['GET'])
    def example_route():
        return "This is an example route."

    app.run(debug=True, host='0.0.0.0', port=5000)
