# piChainLink/data_processor.py

class DataProcessor:
    def process(self, data):
        """Process the data received from the Chainlink oracle."""
        # Check if the data contains the expected structure
        if 'result' in data:
            return self.extract_result(data['result'])
        else:
            raise ValueError("Invalid data format received from oracle.")

    def extract_result(self, result):
        """Extract and transform the result data."""
        # Example transformation logic
        # This can be customized based on the expected structure of the result
        if isinstance(result, dict):
            # If the result is a dictionary, extract relevant fields
            processed_data = {
                "price": result.get("price"),
                "currency": result.get("currency"),
                "timestamp": result.get("timestamp")
            }
            return processed_data
        elif isinstance(result, list):
            # If the result is a list, process each item
            return [self.extract_result(item) for item in result]
        else:
            raise TypeError("Unexpected data type for result.")

    def validate_data(self, data):
        """Validate the processed data."""
        required_fields = ['price', 'currency', 'timestamp']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")
        return True

    def format_data(self, data):
        """Format the processed data for output."""
        # Example formatting logic
        return {
            "status": "success",
            "data": data
        }

# Example usage
if __name__ == "__main__":
    processor = DataProcessor()
    
    # Simulated data received from the Chainlink oracle
    example_data = {
        "result": {
            "price": 2500.50,
            "currency": "ETH",
            "timestamp": "2023-10-01T12:00:00Z"
        }
    }

    try:
        processed_data = processor.process(example_data)
        print("Processed Data:", processed_data)

        # Validate the processed data
        if processor.validate_data(processed_data):
            formatted_data = processor.format_data(processed_data)
            print("Formatted Data:", formatted_data)
    except Exception as e:
        print(f"Error processing data: {e}")
