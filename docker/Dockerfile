FROM python:3.11-slim

WORKDIR /app

# Install system dependencies required by psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements separately to force rebuild of dependencies
COPY requirements.txt /tmp/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy full project AFTER installing dependencies
COPY . .

# Ensure run script is executable
RUN chmod +x docker/run_pipeline.sh

# Default entrypoint
CMD ["sh", "docker/run_pipeline.sh"]



