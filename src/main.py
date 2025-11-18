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


def run_loop(interval):
    while True:
        run_once()
        logger.info(f"Sleeping for {interval} seconds before next run...")
        time.sleep(interval)


if __name__ == "__main__":
    try:
        interval = int(SCHEDULE)
    except:
        interval = 0

    if interval > 0:
        run_loop(interval)
    else:
        run_once()

