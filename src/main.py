from src.extract.tmdb_master_extract import extract_all_categories
from src.transform.transform_movies import transform_movies
from src.transform.transform_movie_details import transform_details
from src.transform.transform_movie_credits import transform_credits

from src.load.load_to_postgres import upsert_movies
from src.load.load_movie_details import upsert_movie_details
from src.load.load_movie_credits import upsert_movie_credits

from src.utils.logger import get_logger
import os

logger = get_logger("main")


def run_once():
    logger.info("=== Starting master TMDB ETL ===")

    movie_ids, movies_raw, details_raw, credits_raw = extract_all_categories()

    df_movies = transform_movies(movies_raw)
    df_details = transform_details(details_raw)
    df_credits = transform_credits(credits_raw)

    upsert_movies(df_movies)
    upsert_movie_details(df_details)
    upsert_movie_credits(df_credits)

    logger.info("=== ETL Completed ===")


if __name__ == "__main__":
    if os.environ.get("GITHUB_ACTIONS") == "true":
        run_once()
    else:
        run_once()







