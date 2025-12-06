FROM python:3.11-slim

# Install system dependencies including FFmpeg
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create directories for uploads and processed files
RUN mkdir -p uploads processed

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the application using Gunicorn
# Render sets the PORT environment variable, default to 10000 if not set
CMD sh -c "gunicorn app:app --bind 0.0.0.0:${PORT:-10000} --timeout 120"
