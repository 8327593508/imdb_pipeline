import os
from src.extract.tmdb_extract import fetch_popular_pages
from src.transform.transform_movies import transform_movies
from src.load.load_to_postgres import upsert_movies
from config.config import MAX_PAGES, SCHEDULE
from src.utils.logger import get_logger

logger = get_logger('main')


def run_once():
    """Run the ETL pipeline exactly once."""
    logger.info("=== Starting pipeline run ===")
    rows = fetch_popular_pages(MAX_PAGES)
    df = transform_movies(rows)
    upsert_movies(df)
    logger.info("=== Pipeline run completed ===")


if __name__ == "__main__":
    # GitHub Actions mode → RUN ONLY ONCE
    if os.environ.get("GITHUB_ACTIONS") == "true":
        run_once()
    else:
        # Local mode
        try:
            interval = int(SCHEDULE)
        except:
            interval = 0

        if interval > 0:
            import time
            while True:
                run_once()
                logger.info(f"Sleeping for {interval} seconds...")
                time.sleep(interval)
        else:
            run_once()


