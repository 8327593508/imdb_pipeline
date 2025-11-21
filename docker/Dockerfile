# docker/Dockerfile

# Base image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies (required for psycopg2 & others)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Run the ETL pipeline
CMD ["python", "-u", "src/main.py"]








