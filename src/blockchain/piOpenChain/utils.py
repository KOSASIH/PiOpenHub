import hashlib
import time
import json

def hash_string(input_string):
    """Generate a SHA-256 hash of the input string."""
    return hashlib.sha256(input_string.encode()).hexdigest()

def get_current_timestamp():
    """Return the current timestamp as an integer."""
    return int(time.time())

def to_json(obj):
    """Convert an object to a JSON string."""
    return json.dumps(obj, default=str, indent=4)

def from_json(json_string):
    """Convert a JSON string back to a Python object."""
    return json.loads(json_string)

def validate_address(address):
    """Basic validation for blockchain addresses."""
    # Example validation: check if the address is a non-empty string
    return isinstance(address, str) and len(address) > 0

def validate_amount(amount):
    """Validate that the amount is a positive number."""
    return isinstance(amount, (int, float)) and amount > 0

# Example usage
if __name__ == "__main__":
    # Test the utility functions
    test_string = "Hello, PiOpenChain!"
    hashed = hash_string(test_string)
    print(f"Hashed string: {hashed}")

    timestamp = get_current_timestamp()
    print(f"Current timestamp: {timestamp}")

    sample_data = {"key": "value", "number": 42}
    json_data = to_json(sample_data)
    print(f"JSON representation: {json_data}")

    parsed_data = from_json(json_data)
    print(f"Parsed data: {parsed_data}")

    address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
    print(f"Is valid address? {validate_address(address)}")

    amount = 100
    print(f"Is valid amount? {validate_amount(amount)}")
