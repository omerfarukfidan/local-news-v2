# Use the official Python image as a base image
FROM python:3.9-slim

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY . /app

# Expose the port Flask will run on
EXPOSE 5000

WORKDIR /app
# Define the command to run the application
CMD ["python", "main.py"]
