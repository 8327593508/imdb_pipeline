from src.utils.db_engine import get_engine
from src.utils.logger import get_logger

logger = get_logger("load_movie_credits")


def upsert_movie_credits(df_credits):
    engine = get_engine()
    conn = engine.raw_connection()
    cursor = conn.cursor()

    for _, row in df_credits.iterrows():   # FIXED

        values = (
            int(row["movie_id"]),
            row["movie_cast"],
            row["movie_crew"]
        )

        cursor.execute("""
            INSERT INTO movie_credits (movie_id, movie_cast, movie_crew)
            VALUES (%s, %s, %s)
            ON CONFLICT (movie_id)
            DO UPDATE SET
                movie_cast = EXCLUDED.movie_cast,
                movie_crew = EXCLUDED.movie_crew;
        """, values)

    conn.commit()
    cursor.close()
    conn.close()
