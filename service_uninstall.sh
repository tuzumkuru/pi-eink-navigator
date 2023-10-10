#!/bin/bash

# Check if the service file exists
SERVICE_FILE="/etc/systemd/system/pi-eink-navigator.service"
if [ -f "$SERVICE_FILE" ]; then
    # Stop and disable the service
    sudo systemctl stop pi-eink-navigator.service
    sudo systemctl disable pi-eink-navigator.service

    # Reload systemd
    sudo systemctl daemon-reload

    # Remove the service file
    sudo rm -f "$SERVICE_FILE"

    echo "Service removed successfully."
else
    echo "Service file not found. It may have already been removed."
fi
