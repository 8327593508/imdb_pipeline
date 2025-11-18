import pandas as pd
from typing import List, Dict
from src.utils.logger import get_logger

logger = get_logger('transform')

def transform_movies(rows: List[Dict]) -> pd.DataFrame:
    """
    Takes raw TMDB movie JSON rows and converts them into a clean DataFrame.
    Only keeps important columns.
    """
    if not rows:
        logger.info("No data received from TMDB to transform.")
        return pd.DataFrame()

    df = pd.DataFrame(rows)

    # columns we want to keep
    columns_to_keep = [
        "id",
        "title",
        "vote_average",
        "vote_count",
        "popularity",
        "release_date",
        "original_language"
    ]

    # ensure all required columns exist
    for col in columns_to_keep:
        if col not in df.columns:
            df[col] = None

    df = df[columns_to_keep]

    # convert release_date to actual date
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce").dt.date

      # 💥 FIX: Remove duplicates by movie ID
    df = df.drop_duplicates(subset="id")

    logger.info(f"Data transformed successfully. Total rows: {len(df)}")

    return df
