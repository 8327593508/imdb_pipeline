from src.utils.db_engine import get_engine

def upsert_movies(movies):
    engine = get_engine()
    with engine.begin() as conn:
        for _, movie in movies.iterrows():
            conn.execute(
                """
                INSERT INTO movies (movie_id, title, popularity, vote_average)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (movie_id)
                DO UPDATE SET
                    title = EXCLUDED.title,
                    popularity = EXCLUDED.popularity,
                    vote_average = EXCLUDED.vote_average;
                """,
                (
                    movie["movie_id"],
                    movie["title"],
                    movie["popularity"],
                    movie["vote_average"]
                )
            )


