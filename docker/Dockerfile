# docker/Dockerfile
FROM python:3.11-slim

# Work inside /app
WORKDIR /app

# System deps for psycopg2 / Postgres
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into the image
COPY . .

# Make sure Python can see the src package
ENV PYTHONPATH=/app

# Run the ETL
CMD ["python", "-u", "src/main.py"]













