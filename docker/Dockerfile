FROM python:3.11-slim

WORKDIR /app

# Install system dependencies needed for psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into the container
COPY . .

# Make the run script executable
RUN chmod +x docker/run_pipeline.sh

# Run the ETL pipeline (with schedule if provided)
CMD ["sh", "docker/run_pipeline.sh"]
