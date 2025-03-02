# utils/errorHandler.py

from flask import jsonify

def handle_error(e):
    """Handle errors and return a JSON response."""
    response = {
        "error": str(e),
        "message": "An error occurred. Please check your input and try again."
    }
    return jsonify(response), 400

# Example usage
if __name__ == "__main__":
    try:
        raise ValueError("This is a test error.")
    except Exception as e:
        response = handle_error(e)
        print(response)  # This would be a Flask response in a real application
