# src/transform/transform_movie_credits.py

import pandas as pd
from src.utils.logger import get_logger

logger = get_logger("transform_movie_credits")


def transform_movie_credits(rows):
    """
    rows is a list of dicts with keys: movie_id, movie_cast, movie_crew
    """
    logger.info(f"Transforming {len(rows)} credit rows...")

    df = pd.DataFrame(rows)

    # Ensure correct column names
    expected_cols = ["movie_id", "movie_cast", "movie_crew"]
    df = df[expected_cols]

    return df
