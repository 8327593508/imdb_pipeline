FROM python:3.11-slim

WORKDIR /app

# Install system deps required for psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    wget \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# --- Copy requirements and install explicitly ---
COPY requirements.txt /tmp/requirements.txt

# Try to install all requirements; if pip returns non-zero,
# show pip output to make debugging simpler.
RUN pip install --no-cache-dir -r /tmp/requirements.txt || (pip --version && echo "pip install -r failed"; pip -V && pip freeze && exit 1)

# Make sure tqdm is installed (install it explicitly as a fallback)
RUN python -m pip install --no-cache-dir tqdm || (echo "explicit tqdm install failed"; pip freeze; exit 1)

# Diagnostic: print installed package summary to build logs
RUN echo "=== PIP FREEZE START ===" && pip freeze | sed -n '1,200p' && echo "=== PIP FREEZE END ==="

# Verify import works at build time (this will fail the build with a clear message if import fails)
RUN python - <<'PY'
try:
    import importlib, pkgutil
    mod = importlib.import_module("tqdm")
    print("tqdm OK, version:", getattr(mod, "__version__", "unknown"))
    print("tqdm module found in:", [m.name for m in pkgutil.iter_modules() if m.name == 'tqdm'])
except Exception as e:
    print("ERROR importing tqdm:", e)
    raise
PY

# Copy full repo after deps are installed
COPY . .

# Make run script executable
RUN chmod +x docker/run_pipeline.sh

CMD ["sh", "docker/run_pipeline.sh"]





