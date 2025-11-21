 feature/multi-file-tmdb
# docker/Dockerfile

 main
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

 feature/multi-file-tmdb
CMD ["python", "-u", "src/main.py"]




# Run the ETL
CMD ["python", "-u", "src/main.py"]
 main






