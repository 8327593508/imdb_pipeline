from src.extract.tmdb_extract import fetch_popular_pages
from src.transform.transform_movies import transform_movies
from src.load.load_to_postgres import upsert_movies
from config.config import MAX_PAGES, SCHEDULE
from src.utils.logger import get_logger
import time

logger = get_logger('main')


def run_once():
    """Runs the pipeline exactly once: Extract → Transform → Load."""
    logger.info("=== Starting pipeline run ===")

    # Extract
    rows = fetch_popular_pages(MAX_PAGES)

    # Transform
    df = transform_movies(rows)

    # Load
    upsert_movies(df)

    logger.info("=== Pipeline run completed ===")


def run_loop():
    """Runs the pipeline repeatedly based on SCHEDULE seconds."""
    if not SCHEDULE:
        run_once()
        return

    try:
        interval = int(SCHEDULE)
    except:
        logger.error("SCHEDULE must be an integer number of seconds.")
        return

    while True:
        run_once()
        logger.info(f"Sleeping for {interval} seconds before next run...")
        time.sleep(interval)


if __name__ == "__main__":
    if SCHEDULE:
        run_loop()
    else:
        run_once()
