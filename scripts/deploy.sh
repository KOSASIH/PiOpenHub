#!/bin/bash

# deploy.sh - Deployment script for PiOpenHub

# Exit immediately if a command exits with a non-zero status
set -e

# Define variables
REPO_URL="https://github.com/yourusername/PiOpenHub.git"
APP_DIR="/path/to/piopenhub"  # Change this to your application directory
BRANCH="main"                  # Change this to your desired branch

# Navigate to the application directory
cd $APP_DIR

# Pull the latest code from the repository
echo "Pulling latest code from $REPO_URL..."
git pull origin $BRANCH

# Install dependencies
if [ -f requirements.txt ]; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
fi

if [ -f package.json ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

# Run database migrations
echo "Running database migrations..."
if [ -d "src/database/migrations" ]; then
    # Assuming a Python migration script
    python src/database/migrations/migrate.py
fi

# Start the application
echo "Starting the application..."
if [ -f "src/main/app.py" ]; then
    python src/main/app.py &
elif [ -f "src/main/index.js" ]; then
    node src/main/index.js &
fi

echo "Deployment completed successfully!"
