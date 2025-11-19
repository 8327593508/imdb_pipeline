# src/main.py
import os
import pandas as pd

from src.extract.tmdb_master_extract import extract_all_categories
from src.utils.logger import get_logger

logger = get_logger("main")


def run_once():
    logger.info("=== Starting FULL TMDB extraction ===")

    # Extract 4 datasets
    df_popular, df_top, df_upcoming, df_trending = extract_all_categories(
        pages_popular=MAX_PAGES,
        pages_top=MAX_PAGES,
        pages_upcoming=30,
        pages_trending=30
    )

    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    # Save 4 separate CSVs
    df_popular.to_csv("data/popular_movies.csv", index=False)
    df_top.to_csv("data/top_rated_movies.csv", index=False)
    df_upcoming.to_csv("data/upcoming_movies.csv", index=False)
    df_trending.to_csv("data/trending_movies.csv", index=False)

    logger.info("Saved all CSV files successfully!")
    logger.info("=== Extraction completed ===")


if __name__ == "__main__":
    # Force run ONCE in GitHub Actions
    if os.environ.get("GITHUB_ACTIONS") == "true":
        run_once()
    else:
        # Local mode: always run once
        run_once()





