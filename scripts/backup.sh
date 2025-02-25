#!/bin/bash

# backup.sh - Backup script for PiOpenHub

# Exit immediately if a command exits with a non-zero status
set -e

# Define variables
BACKUP_DIR="/path/to/backup"  # Change this to your backup directory
APP_DIR="/path/to/piopenhub"   # Change this to your application directory
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Backup the database
echo "Backing up the database..."
if [ -f "src/database/db_backup.sh" ]; then
    bash src/database/db_backup.sh $BACKUP_DIR/db_backup_$TIMESTAMP.sql
else
    echo "Database backup script not found!"
fi

# Backup application files
echo "Backing up application files..."
tar -czf $BACKUP_DIR/piopenhub_backup_$TIMESTAMP.tar.gz -C $APP_DIR .

echo "Backup completed successfully! Backup files are located in $BACKUP_DIR."
