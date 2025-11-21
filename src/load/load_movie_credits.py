from src.utils.db_engine import get_engine
from src.utils.logger import get_logger
import json

logger = get_logger("load_movie_credits")


def load_movie_credits(rows: list[dict]):
    """Load movie credits into PostgreSQL."""
    engine = get_engine()

    insert_sql = """
        INSERT INTO movie_credits (movie_id, movie_cast, movie_crew)
        VALUES (%s, %s, %s)
        ON CONFLICT (movie_id) DO UPDATE SET
            movie_cast = EXCLUDED.movie_cast,
            movie_crew = EXCLUDED.movie_crew;
    """

    with engine.connect() as conn:
        for row in rows:
            conn.execute(
                insert_sql,
                (
                    row["movie_id"],
                    json.dumps(row["movie_cast"]),  # UPDATED
                    json.dumps(row["movie_crew"])   # UPDATED
                )
            )

    logger.info(f"Inserted/Updated {len(rows)} credit rows.")


