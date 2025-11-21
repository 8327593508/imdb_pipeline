from sqlalchemy import create_engine
from config.config import PG_USER, PG_PASSWORD, PG_PORT, PG_DB


def get_engine():
    """
    Creates a SQLAlchemy engine connected to the Postgres container.
    Hostname 'postgres' matches docker-compose service name.
    """
    url = f"postgresql://{PG_USER}:{PG_PASSWORD}@postgres:{PG_PORT}/{PG_DB}"
    return create_engine(url)
