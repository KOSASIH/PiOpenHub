#!/bin/bash

# Clean script for removing temporary files and directories

# Function to print messages
function print_message {
    echo "=============================="
    echo "$1"
    echo "=============================="
}

# Define directories and files to clean
TEMP_DIRS=("venv" "results" "logs" "tmp")
TEMP_FILES=("*.pyc" "*.pyo" "__pycache__")

# Clean up temporary directories
for dir in "${TEMP_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        print_message "Removing directory: $dir"
        rm -rf "$dir"
    else
        print_message "Directory $dir not found. Skipping."
    fi
done

# Clean up temporary files
for pattern in "${TEMP_FILES[@]}"; do
    print_message "Removing files matching pattern: $pattern"
    find . -name "$pattern" -exec rm -f {} +
done

# Additional cleanup tasks can be added here
# For example, removing specific log files or temporary data files

print_message "Cleanup complete."
