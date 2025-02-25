# loggingMiddleware.py

import logging
from flask import request, g

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def logging_middleware(app):
    """Logging middleware to log requests and responses."""
    
    @app.before_request
    def before_request():
        """Log the incoming request details."""
        g.start_time = time.time()  # Record the start time
        logger.info(f"Request: {request.method} {request.url}")

    @app.after_request
    def after_request(response):
        """Log the response details."""
        duration = time.time() - g.start_time  # Calculate the duration
        logger.info(f"Response: {response.status} | Duration: {duration:.2f}s")
        return response

    @app.errorhandler(Exception)
    def handle_exception(e):
        """Log any exceptions that occur during request processing."""
        logger.error(f"Error: {str(e)}")
        return "Internal Server Error", 500

# Example of how to use the middleware in your main application
if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)

    # Register the logging middleware
    logging_middleware(app)

    @app.route('/example', methods=['GET'])
    def example_route():
        return "This is an example route."

    app.run(debug=True, host='0.0.0.0', port=5000)
