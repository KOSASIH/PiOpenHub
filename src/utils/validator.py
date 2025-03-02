# utils/validator.py

def validate_partner_info(partner_info):
    """Validate partner information."""
    if 'name' not in partner_info or 'api_endpoint' not in partner_info:
        raise ValueError("Partner information must include 'name' and 'api_endpoint'.")
    if not isinstance(partner_info['name'], str) or not isinstance(partner_info['api_endpoint'], str):
        raise ValueError("Both 'name' and 'api_endpoint' must be strings.")

def validate_data(data):
    """Validate input data for predictions."""
    if not isinstance(data, list) or not all(isinstance(item, list) for item in data):
        raise ValueError("Input data must be a list of lists.")
    if not all(len(item) > 0 for item in data):
        raise ValueError("Each item in input data must be a non-empty list.")

# Example usage
if __name__ == "__main__":
    try:
        validate_partner_info({'name': 'IBM', 'api_endpoint': 'https://api.ibm.com/data'})
        print("Partner info is valid.")
    except ValueError as e:
        print(f"Validation error: {e}")
