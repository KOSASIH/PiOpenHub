#!/bin/bash

# setup.sh - Setup script for PiOpenHub

# Exit immediately if a command exits with a non-zero status
set -e

# Define variables
APP_DIR="/path/to/piopenhub"  # Change this to your application directory

# Navigate to the application directory
cd $APP_DIR

# Install dependencies
if [ -f requirements.txt ]; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
fi

if [ -f package.json ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

# Set up the database
echo "Setting up the database..."
if [ -d "src/database/migrations" ]; then
    # Assuming a Python migration script
    python src/database/migrations/migrate.py
fi

# Seed the database with initial data (if applicable)
if [ -d "src/database/seeders" ]; then
    echo "Seeding the database..."
    python src/database/seeders/seed.py  # Adjust as necessary
fi

echo "Setup completed successfully! You can now run the application."
