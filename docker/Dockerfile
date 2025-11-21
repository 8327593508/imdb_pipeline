FROM python:3.11-slim

WORKDIR /app

# System deps for psycopg2 / Postgres
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Make sure Python can import the src package
ENV PYTHONPATH=/app

# Run ETL via src.main as a module
CMD ["python", "-m", "src.main"]








