# src/main.py

import os
from config.config import MAX_PAGES, SCHEDULE
from src.extract.tmdb_master_extract import extract_all_categories
from src.transform.transform_movies import transform_movies
from src.transform.transform_movie_details import transform_movie_details
from src.transform.transform_movie_credits import transform_movie_credits
from src.load.load_to_postgres import upsert_movies
from src.load.load_movie_details import upsert_movie_details
from src.load.load_movie_credits import upsert_movie_credits
from src.utils.logger import get_logger
import time

logger = get_logger("main")


def run_once():
    logger.info("=== Starting TMDB multi-file ETL run ===")

    data = extract_all_categories(pages_popular=MAX_PAGES)

    # Use only 'popular' list for the popular_movies table
    popular_movies = data["popular"]
    details_list = data["details"]
    credits_list = data["credits"]

    logger.info(f"Transforming {len(popular_movies)} popular movies...")
    df_movies = transform_movies(popular_movies)

    logger.info(f"Transforming {len(details_list)} movie details...")
    df_details = transform_movie_details(details_list)

    logger.info(f"Transforming {len(credits_list)} movie credits...")
    df_credits = transform_movie_credits(credits_list)

    logger.info("Loading into Postgres...")
    upsert_movies(df_movies)
    upsert_movie_details(df_details)
    upsert_movie_credits(df_credits)

    logger.info("=== ETL COMPLETED SUCCESSFULLY ===")


def run_loop():
    """Local-only: repeatedly run ETL based on SCHEDULE seconds."""
    try:
        interval = int(SCHEDULE)
    except Exception:
        logger.error("SCHEDULE must be an integer number of seconds.")
        return

    while True:
        run_once()
        logger.info(f"Sleeping for {interval} seconds before next run...")
        time.sleep(interval)


if __name__ == "__main__":
    # In GitHub Actions we set GITHUB_ACTIONS=true and SCHEDULE=0 so it runs once.
    if os.environ.get("GITHUB_ACTIONS") == "true":
        run_once()
    else:
        if SCHEDULE and str(SCHEDULE).isdigit() and int(SCHEDULE) > 0:
            run_loop()
        else:
            run_once()









