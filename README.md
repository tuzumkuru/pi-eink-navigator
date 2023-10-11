# Raspberry Pi E-Ink Navigator

## Introduction

The Raspberry Pi E-Ink Navigator is a Python project that utilizes a Raspberry Pi and an E-Ink display to create a customizable information display system. The project allows you to display various screens with information, such as weather, images, and more, on an E-Ink display.

## Prerequisites

Before running the project, you will need the following:

- Raspberry Pi (with an internet connection)
- E-Ink display (e.g., Adafruit E-Ink display)
- Python 3 installed on your Raspberry Pi
- Python 3 Virtual Environment (`python3-venv`)

## Installation

1. Clone this repository to your Raspberry Pi.

    ```bash
    git clone https://github.com/tuzumkuru/pi-eink-navigator.git
    ```

2. Navigate to the project directory:

    ```bash
    cd pi-eink-navigator
    ```

3. Run the installation script to set up the project and create a systemd service.

    ```bash
    bash service_install.sh
    ```

## Usage

1. Start the E-Ink Navigator service.

    ```bash
    sudo systemctl start pi-eink-navigator.service
    ```

2. The service will run and display screens on the E-Ink display.

3. You can access the project's code in the project directory. Customize the screens and functionality to your needs.

## Uninstallation

If you want to remove the service:

1. Run the uninstallation script:

    ```bash
    bash service_uninstall.sh
    ```

2. The service will be stopped, disabled, and removed.

## Contributing

Feel free to contribute to this project by creating new screens or improving existing ones. Submit a pull request if you'd like to share your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
