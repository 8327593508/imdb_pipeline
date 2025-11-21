# src/transform/transform_movies.py

import pandas as pd
from src.utils.logger import get_logger

logger = get_logger("transform_movies")


def transform_movies(rows):
    logger.info(f"Transforming {len(rows)} popular movies...")

    # TMDB returns 'id', 'title', 'vote_average', etc.
    df = pd.DataFrame(rows)

    # Keep only the columns you need
    expected_cols = [
        "id",
        "title",
        "vote_average",
        "vote_count",
        "popularity",
        "release_date",
        "original_language",
    ]
    df = df[expected_cols]

    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")

    return df
