# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir elasticsearch nltk python-dotenv

# Download NLTK data
RUN python -c "import nltk; nltk.download('punkt', quiet=True)"


# Run script.py when the container launches
ENTRYPOINT ["python", "find-boilerplate.py"]
