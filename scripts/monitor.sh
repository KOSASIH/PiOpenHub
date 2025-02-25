#!/bin/bash

# Monitoring script for system health

LOG_FILE="system_health.log"

# Function to log the current date and time
log_time() {
    echo "$(date '+%Y-%m-%d %H:%M:%S')"
}

# Function to check CPU usage
check_cpu() {
    CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
    echo "CPU Usage: $CPU_USAGE%"
}

# Function to check memory usage
check_memory() {
    MEM_TOTAL=$(free | grep Mem | awk '{print $2}')
    MEM_USED=$(free | grep Mem | awk '{print $3}')
    MEM_USAGE=$(echo "scale=2; $MEM_USED/$MEM_TOTAL*100" | bc)
    echo "Memory Usage: $MEM_USAGE%"
}

# Function to check disk space
check_disk() {
    DISK_USAGE=$(df -h | grep '^/dev/' | awk '{print $5}' | sed 's/%//g' | sort -n | tail -1)
    echo "Disk Usage: $DISK_USAGE%"
}

# Main monitoring loop
while true; do
    echo "$(log_time) - System Health Check" >> $LOG_FILE
    check_cpu >> $LOG_FILE
    check_memory >> $LOG_FILE
    check_disk >> $LOG_FILE
    echo "----------------------------------------" >> $LOG_FILE
    sleep 60  # Check every 60 seconds
done
