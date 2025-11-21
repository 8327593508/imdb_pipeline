from sqlalchemy import create_engine
from config.config import PG_USER, PG_PASSWORD, PG_DB

DB_URL = f"postgresql://{PG_USER}:{PG_PASSWORD}@imdb_pipeline_postgres:5432/{PG_DB}"

def get_engine():
    return create_engine(DB_URL)
