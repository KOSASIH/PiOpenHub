import logging
from flask import jsonify

# Set up logging
logging.basicConfig(level=logging.INFO)

class APIException(Exception):
    """Base class for API exceptions."""
    status_code = 500
    message = "An unexpected error occurred."

    def __init__(self, message=None, status_code=None):
        if message:
            self.message = message
        if status_code:
            self.status_code = status_code
        super().__init__(self.message)

class NotFoundException(APIException):
    """Exception raised for not found errors."""
    status_code = 404
    message = "Resource not found."

class BadRequestException(APIException):
    """Exception raised for bad request errors."""
    status_code = 400
    message = "Bad request."

class UnauthorizedException(APIException):
    """Exception raised for unauthorized access errors."""
    status_code = 401
    message = "Unauthorized access."

class InternalServerErrorException(APIException):
    """Exception raised for internal server errors."""
    status_code = 500
    message = "Internal server error."

def handle_error(error):
    """Centralized error handling function."""
    if isinstance(error, APIException):
        response = {
            "status": "error",
            "message": error.message,
            "code": error.status_code
        }
        logging.error(f"{error.status_code} - {error.message}")
        return jsonify(response), error.status_code

    # Handle unexpected errors
    logging.error(f"500 - {str(error)}")
    response = {
        "status": "error",
        "message": "An unexpected error occurred.",
        "code": 500
    }
    return jsonify(response), 500

# Example usage in a Flask app
if __name__ == "__main__":
    from flask import Flask

    app = Flask(__name__)

    @app.errorhandler(APIException)
    def api_exception_handler(error):
        return handle_error(error)

    @app.errorhandler(Exception)
    def general_exception_handler(error):
        return handle_error(error)

    @app.route('/example')
    def example_route():
        raise NotFoundException("The requested resource was not found.")

    @app.route('/bad-request')
    def bad_request_route():
        raise BadRequestException("The request parameters are invalid.")

    @app.route('/unauthorized')
    def unauthorized_route():
        raise UnauthorizedException("You do not have permission to access this resource.")

    @app.route('/internal-error')
    def internal_error_route():
        raise InternalServerErrorException("An internal error occurred.")

    if __name__ == '__main__':
        app.run(debug=True)
