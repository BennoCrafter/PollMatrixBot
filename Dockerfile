# Use a Python base image
FROM python:3.11.2-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Define the command to run the application
CMD ["python", "main.py"]
