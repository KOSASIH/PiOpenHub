#!/bin/bash

# Update script for quantum computing and AI projects

# Function to print messages
function print_message {
    echo "=============================="
    echo "$1"
    echo "=============================="
}

# Update package list and install necessary packages
print_message "Updating package list and installing necessary packages..."

# Update package list
sudo apt-get update

# Install Python and pip if not already installed
if ! command -v python3 &> /dev/null; then
    print_message "Python3 not found. Installing Python3..."
    sudo apt-get install -y python3 python3-pip
else
    print_message "Python3 is already installed."
fi

# Install virtualenv if not already installed
if ! command -v virtualenv &> /dev/null; then
    print_message "virtualenv not found. Installing virtualenv..."
    sudo pip3 install virtualenv
else
    print_message "virtualenv is already installed."
fi

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_message "Creating a virtual environment..."
    virtualenv venv
else
    print_message "Virtual environment already exists."
fi

# Activate the virtual environment
source venv/bin/activate

# Install required Python packages
print_message "Installing required Python packages..."
pip install -r requirements.txt

# Install Qiskit if not already installed
if ! python -c "import qiskit" &> /dev/null; then
    print_message "Qiskit not found. Installing Qiskit..."
    pip install qiskit
else
    print_message "Qiskit is already installed."
fi

# Install any other dependencies as needed
# Add additional package installations here

print_message "Update complete. Your environment is ready to use!"

# Deactivate the virtual environment
deactivate
