from src.utils.db_engine import get_engine
from src.utils.logger import get_logger

logger = get_logger("load_to_postgres")


def upsert_movies(df_movies):
    engine = get_engine()
    conn = engine.raw_connection()
    cursor = conn.cursor()

    for _, movie in df_movies.iterrows():     # FIXED

        values = (
            int(movie["movie_id"]),
            movie["title"],
            movie["overview"],
            float(movie["popularity"]) if movie["popularity"] else 0,
            movie["release_date"]
        )

        cursor.execute("""
            INSERT INTO movies (movie_id, title, overview, popularity, release_date)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (movie_id)
            DO UPDATE SET
                title = EXCLUDED.title,
                overview = EXCLUDED.overview,
                popularity = EXCLUDED.popularity,
                release_date = EXCLUDED.release_date;
        """, values)

    conn.commit()
    cursor.close()
    conn.close()
