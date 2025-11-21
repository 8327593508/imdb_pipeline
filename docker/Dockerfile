FROM python:3.11-slim

WORKDIR /app

# Fix pip + ensure cache is clean
RUN pip install --upgrade pip && pip cache purge

# Install system deps
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy ONLY requirements first (better caching)
COPY requirements.txt .

# Force install INCLUDING tqdm
RUN pip install --no-cache-dir -r requirements.txt
RUN pip show tqdm || (echo "tqdm missing!" && exit 1)

# Now copy project files
COPY . .

CMD ["python", "src/main.py"]






