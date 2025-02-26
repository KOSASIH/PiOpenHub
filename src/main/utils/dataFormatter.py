import json
import logging
from typing import Any, Dict, List, Union

# Set up logging
logging.basicConfig(level=logging.INFO)

class DataFormatter:
    @staticmethod
    def to_json(data: Any) -> str:
        """Convert data to JSON format."""
        try:
            json_data = json.dumps(data, default=str)  # Convert to JSON, handling non-serializable types
            logging.info("Data successfully converted to JSON.")
            return json_data
        except (TypeError, ValueError) as e:
            logging.error(f"Error converting data to JSON: {e}")
            raise

    @staticmethod
    def format_response(data: Any, status: str = "success", message: str = "") -> Dict[str, Any]:
        """Format the API response."""
        response = {
            "status": status,
            "message": message,
            "data": data
        }
        logging.info("Response formatted successfully.")
        return response

    @staticmethod
    def validate_data(data: Dict[str, Any], required_fields: List[str]) -> bool:
        """Validate that the required fields are present in the data."""
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            logging.warning(f"Missing required fields: {missing_fields}")
            return False
        logging.info("Data validation successful.")
        return True

    @staticmethod
    def format_list(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format a list of dictionaries for API response."""
        formatted_list = []
        for item in data:
            formatted_item = {key: str(value) for key, value in item.items()}  # Convert all values to string
            formatted_list.append(formatted_item)
        logging.info("List formatted successfully.")
        return formatted_list

    @staticmethod
    def format_error(message: str, code: int = 400) -> Dict[str, Any]:
        """Format an error response."""
        error_response = {
            "status": "error",
            "message": message,
            "code": code
        }
        logging.error(f"Error response formatted: {message}")
        return error_response

# Example usage
if __name__ == "__main__":
    formatter = DataFormatter()

    # Example data
    example_data = {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com"
    }

    # Convert to JSON
    json_data = formatter.to_json(example_data)
    print("JSON Data:", json_data)

    # Format response
    response = formatter.format_response(example_data, message="User retrieved successfully.")
    print("Formatted Response:", response)

    # Validate data
    is_valid = formatter.validate_data(example_data, required_fields=["id", "name", "email"])
    print("Is Data Valid:", is_valid)

    # Format list
    example_list = [
        {"id": 1, "name": "John Doe"},
        {"id": 2, "name": "Jane Smith"}
    ]
    formatted_list = formatter.format_list(example_list)
    print("Formatted List:", formatted_list)

    # Format error
    error_response = formatter.format_error("User not found", code=404)
    print("Error Response:", error_response)
