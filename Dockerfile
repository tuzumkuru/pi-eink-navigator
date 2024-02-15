FROM python:3.9-slim

# Install necessary system packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        fonts-dejavu \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the entire application code
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the application
CMD ["python", "main.py"]
