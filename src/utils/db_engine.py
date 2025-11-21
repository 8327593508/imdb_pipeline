from sqlalchemy import create_engine
from config.config import PG_USER, PG_PASSWORD, PG_DB, PG_PORT
import os

# Get PG_HOST from environment (docker-compose sets it), default to localhost
PG_HOST = os.getenv("PG_HOST", "localhost")

DB_URL = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

def get_engine():
    """Create and return a SQLAlchemy engine for PostgreSQL."""
    try:
        engine = create_engine(DB_URL, pool_pre_ping=True)
        return engine
    except Exception as e:
        print(f"Error creating database engine: {e}")
        raise
