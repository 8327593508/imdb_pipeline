# src/main.py

import os
from src.extract.tmdb_master_extract import (
    extract_all_movie_ids,
    extract_all_categories,
)
from src.transform.transform_movies import transform_movies
from src.transform.transform_movie_details import transform_movie_details
from src.transform.transform_movie_credits import transform_movie_credits
from src.load.load_to_postgres import upsert_movies
from src.load.load_movie_details import upsert_movie_details
from src.load.load_movie_credits import upsert_movie_credits
from src.utils.logger import get_logger

logger = get_logger("main")


def run_once():
    logger.info("=== Starting TMDB Multi-File ETL ===")

    # Step 1: Collect movie IDs
    movie_ids = extract_all_movie_ids()

    # Step 2: Fetch details + credits
    details, credits = extract_all_categories(movie_ids)

    # Step 3: Transform all
    df_movies = transform_movies(movie_ids)
    df_details = transform_movie_details(details)
    df_credits = transform_movie_credits(credits)

    # Step 4: Load all
    upsert_movies(df_movies)
    upsert_movie_details(df_details)
    upsert_movie_credits(df_credits)

    logger.info("=== ETL COMPLETED SUCCESSFULLY ===")


if __name__ == "__main__":
    run_once()








