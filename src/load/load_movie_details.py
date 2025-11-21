from src.utils.db_engine import get_engine
from src.utils.logger import get_logger

logger = get_logger("load_movie_details")


def upsert_movie_details(df_details):
    engine = get_engine()
    conn = engine.raw_connection()
    cursor = conn.cursor()

    for _, row in df_details.iterrows():   # FIXED

        values = (
            int(row["movie_id"]),
            row["genres"],
            row["runtime"],
            row["budget"],
            row["revenue"]
        )

        cursor.execute("""
            INSERT INTO movie_details (movie_id, genres, runtime, budget, revenue)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (movie_id)
            DO UPDATE SET
                genres = EXCLUDED.genres,
                runtime = EXCLUDED.runtime,
                budget = EXCLUDED.budget,
                revenue = EXCLUDED.revenue;
        """, values)

    conn.commit()
    cursor.close()
    conn.close()
