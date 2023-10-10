#!/bin/bash

# Check if python3-venv is installed
if ! dpkg -l | grep -q python3-venv; then
    echo "Error: python3-venv is not installed. Please install it using 'sudo apt-get install python3-venv' and run the script again."
    exit 1
fi

# Get the current directory of the script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Print progress message
echo "1. Checking python3-venv installation... Done"

# Navigate to the project directory
cd "$DIR"

# Print progress message
echo "2. Navigating to the project directory... Done"

# Create a virtual environment in a .venv folder
python3 -m venv .venv

# Print progress message
echo "3. Creating a virtual environment... Done"

# Activate the virtual environment
source .venv/bin/activate

# Print progress message
echo "4. Activating the virtual environment... Done"

# Install Python packages from requirements.txt inside the virtual environment
pip install -r requirements.txt

# Print progress message
echo "5. Installing Python packages... Done"

# Create a systemd service file
sudo tee /etc/systemd/system/pi-eink-navigator.service > /dev/null <<EOF
[Unit]
Description=e-Ink Navigator for Raspberry Pi's
Wants=network-online.target

[Service]
WorkingDirectory=$DIR
ExecStart=$DIR/.venv/bin/python3 $DIR/main.py
Restart=always
RestartSec=30
After=network-online.target

[Install]
WantedBy=multi-user.target
EOF

# Check if the service file was created successfully
if [ -f /etc/systemd/system/pi-eink-navigator.service ]; then
    echo "6. Creating a systemd service file... Done"
else
    echo "Error: Failed to create the service file."
    exit 1
fi

# Reload systemd and enable the service
sudo systemctl daemon-reload
sudo systemctl enable pi-eink-navigator.service

# Print progress message
echo "7. Reloading systemd and enabling the service... Done"

# Print some information
echo "The e-Ink Navigator service has been installed and enabled."
echo "You can start the service using 'sudo systemctl start pi-eink-navigator.service'."
