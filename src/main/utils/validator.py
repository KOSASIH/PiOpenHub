import re

class Validator:
    def __init__(self):
        pass

    @staticmethod
    def is_required(value):
        """Check if a value is required and not empty."""
        if value is None or (isinstance(value, str) and value.strip() == ''):
            return False
        return True

    @staticmethod
    def is_email(value):
        """Validate if the value is a valid email address."""
        if not Validator.is_required(value):
            return False
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, value) is not None

    @staticmethod
    def is_phone(value):
        """Validate if the value is a valid phone number."""
        if not Validator.is_required(value):
            return False
        phone_regex = r'^\+?[1-9]\d{1,14}$'  # E.164 format
        return re.match(phone_regex, value) is not None

    @staticmethod
    def is_integer(value):
        """Check if the value is an integer."""
        if not Validator.is_required(value):
            return False
        return isinstance(value, int)

    @staticmethod
    def is_float(value):
        """Check if the value is a float."""
        if not Validator.is_required(value):
            return False
        return isinstance(value, float)

    @staticmethod
    def is_in_list(value, valid_list):
        """Check if the value is in a predefined list."""
        if not Validator.is_required(value):
            return False
        return value in valid_list

    @staticmethod
    def validate_user_data(user_data):
        """Validate user data dictionary."""
        errors = {}
        
        if not Validator.is_required(user_data.get('username')):
            errors['username'] = 'Username is required.'
        
        if not Validator.is_email(user_data.get('email')):
            errors['email'] = 'Invalid email address.'
        
        if not Validator.is_phone(user_data.get('phone')):
            errors['phone'] = 'Invalid phone number.'
        
        if not Validator.is_integer(user_data.get('age')):
            errors['age'] = 'Age must be an integer.'
        
        return errors

# Example usage
if __name__ == "__main__":
    validator = Validator()
    
    # Validate email
    email = "test@example.com"
    print(f"Is '{email}' a valid email? {validator.is_email(email)}")
    
    # Validate user data
    user_data = {
        'username': 'john_doe',
        'email': 'john.doe@example.com',
        'phone': '+1234567890',
        'age': 30
    }
    
    validation_errors = validator.validate_user_data(user_data)
    if validation_errors:
        print("Validation errors:", validation_errors)
    else:
        print("User data is valid.")
