# docker/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy requirements from project root (one level up)
COPY ../requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project root into the container
COPY ../ .

CMD ["python", "-u", "src/main.py"]










