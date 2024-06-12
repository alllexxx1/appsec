# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWEITEBYTECODE 1

# Install Poetry
RUN pip install poetry

# Set the working directory
WORKDIR /app

# Copy the project files into the Docker image
COPY . .

# Install dependencies
RUN poetry config virtualenvs.create false
RUN poetry config installer.max-workers 1
RUN poetry install --no-dev

# Expose the port Flask is running on
EXPOSE 5000

# Command to run the application
CMD ["python", "main.py"]
