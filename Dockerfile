# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY . .

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which the Flask app will run
EXPOSE 80

# Run the Flask application using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:80", "102117161prog:app"]
