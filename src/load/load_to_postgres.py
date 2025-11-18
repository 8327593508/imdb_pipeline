from src.utils.db_engine import get_engine
from sqlalchemy import text
import pandas as pd
from src.utils.logger import get_logger

logger = get_logger('load')


def ensure_table(engine):
    """
    Creates the popular_movies table if it doesn't exist.
    """
    ddl = '''
    CREATE TABLE IF NOT EXISTS popular_movies (
        id BIGINT PRIMARY KEY,
        title TEXT,
        vote_average DOUBLE PRECISION,
        vote_count BIGINT,
        popularity DOUBLE PRECISION,
        release_date DATE,
        original_language TEXT,
        last_updated TIMESTAMP DEFAULT now()
    );
    '''
    with engine.begin() as conn:
        conn.execute(text(ddl))


def upsert_movies(df: pd.DataFrame, table_name: str = 'popular_movies'):
    """
    Inserts / updates movies into PostgreSQL.
    Uses a temporary table + ON CONFLICT (id) DO UPDATE.
    """
    if df.empty:
        logger.info("No data to load into PostgreSQL.")
        return

    engine = get_engine()

    # 1. make sure table exists
    ensure_table(engine)

    with engine.begin() as conn:
        # 2. write dataframe to temporary table
        df.to_sql('tmp_popular_movies', conn, if_exists='replace', index=False)

        # 3. UPSERT from temp table into main table
        upsert_sql = f"""
        INSERT INTO {table_name} 
          (id, title, vote_average, vote_count, popularity, release_date, original_language, last_updated)
        SELECT 
          id, title, vote_average, vote_count, popularity, release_date, original_language, NOW()
        FROM tmp_popular_movies
        ON CONFLICT (id) DO UPDATE SET
          title = EXCLUDED.title,
          vote_average = EXCLUDED.vote_average,
          vote_count = EXCLUDED.vote_count,
          popularity = EXCLUDED.popularity,
          release_date = EXCLUDED.release_date,
          original_language = EXCLUDED.original_language,
          last_updated = NOW();

        DROP TABLE IF EXISTS tmp_popular_movies;
        """

        conn.execute(text(upsert_sql))

    logger.info(f"Upserted {len(df)} rows into table '{table_name}'.")
