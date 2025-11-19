from src.extract.tmdb_master_extract import extract_all_categories
from src.transform.transform_movies import transform_movies
from src.load.load_to_postgres import upsert_movies
from src.utils.logger import get_logger

logger = get_logger("main")

def run_once():
    logger.info("=== Starting multi-file ETL ===")

    data = extract_all_categories(
        pages_popular=200,
        pages_top=200,
        pages_upcoming=50,
        pages_trending=50
    )

    # Save CSVs
    data["movies"].to_csv("data/movies.csv", index=False)
    data["credits"].to_csv("data/credits.csv", index=False)

    # Load to DB (optional)
    upsert_movies(data["movies"])

    logger.info("=== ETL Completed ===")

if __name__ == "__main__":
    run_once()






