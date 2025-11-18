import os
from src.extract.tmdb_extract import fetch_popular_pages
from src.transform.transform_movies import transform_movies
from src.load.load_to_postgres import upsert_movies
from config.config import MAX_PAGES, SCHEDULE
from src.utils.logger import get_logger
import time

logger = get_logger('main')


def run_once():
    logger.info("=== Starting pipeline run ===")
    rows = fetch_popular_pages(MAX_PAGES)
    df = transform_movies(rows)
    upsert_movies(df)
    logger.info("=== Pipeline run completed ===")


if __name__ == "__main__":
    # When running inside GitHub Actions → always run ONCE
    if os.environ.get("GITHUB_ACTIONS"):
        run_once()

    # Local mode
    else:
        if SCHEDULE and int(SCHEDULE) > 0:
            while True:
                run_once()
                logger.info(f"Sleeping for {SCHEDULE} seconds...")
                time.sleep(int(SCHEDULE))
        else:
            run_once()


