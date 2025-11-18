from sqlalchemy import create_engine
from config.config import PG_USER, PG_PASSWORD, PG_HOST, PG_PORT, PG_DB

def get_engine():
    url = f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}?sslmode=disable"
    return create_engine(url)
