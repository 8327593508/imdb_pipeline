import pandas as pd
from sqlalchemy import text
from src.utils.db_engine import get_engine

engine = get_engine()


def upsert_movie_credits(credits_data: list[dict]):
    """
    Inserts or updates movie credits (cast + crew) into PostgreSQL.
    """
    if not credits_data:
        print("No credits data to insert.")
        return

    df = pd.DataFrame(credits_data)

    # Ensure JSON-friendly structures
    df["movie_cast"] = df["movie_cast"].apply(lambda x: x if isinstance(x, list) else [])
    df["movie_crew"] = df["movie_crew"].apply(lambda x: x if isinstance(x, list) else [])

    upsert_query = """
    INSERT INTO movie_credits (movie_id, movie_cast, movie_crew)
    VALUES (:movie_id, :movie_cast, :movie_crew)
    ON CONFLICT (movie_id)
    DO UPDATE SET 
        movie_cast = EXCLUDED.movie_cast,
        movie_crew = EXCLUDED.movie_crew;
    """

    with engine.begin() as conn:
        conn.execute(
            text(upsert_query),
            df.to_dict(orient="records")
        )

    print(f"Inserted/updated {len(df)} movie credits records.")
