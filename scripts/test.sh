#!/bin/bash

# Test script for running all tests in the quantum computing and AI projects

# Function to print messages
function print_message {
    echo "=============================="
    echo "$1"
    echo "=============================="
}

# Activate the virtual environment
if [ -d "venv" ]; then
    print_message "Activating the virtual environment..."
    source venv/bin/activate
else
    print_message "Virtual environment not found. Please create it first using update.sh."
    exit 1
fi

# Run unit tests
print_message "Running unit tests..."
if [ -d "tests" ]; then
    # Discover and run all tests in the tests directory
    python -m unittest discover -s tests -p "*.py"
else
    print_message "No tests directory found. Please create a 'tests' directory with your test files."
    exit 1
fi

# Run additional tests if needed
# Uncomment and modify the following lines to run other test suites or scripts
# print_message "Running integration tests..."
# python tests/integration_tests.py

# print_message "Running end-to-end tests..."
# python tests/e2e_tests.py

# Deactivate the virtual environment
print_message "Deactivating the virtual environment..."
deactivate

print_message "All tests completed."
