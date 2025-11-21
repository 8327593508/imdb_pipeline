FROM python:3.10-slim

WORKDIR /app

# Copy requirements first
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy ENTIRE project (INCLUDING src folder)
COPY . .

# Ensure Python can import the src package
ENV PYTHONPATH="/app"

CMD ["python", "-u", "src/main.py"]







