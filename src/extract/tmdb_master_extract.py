# src/extract/tmdb_master_extract.py

from src.extract.tmdb_extract_movies import (
    fetch_popular_movies,
    fetch_top_rated_movies,
    fetch_upcoming_movies,
    fetch_trending_movies,
)

from src.extract.tmdb_extract_details import fetch_movie_details
from src.extract.tmdb_extract_credits import fetch_movie_credits
import time
from src.utils.logger import get_logger

logger = get_logger("tmdb_master_extract")


# STEP 1 — Fetch MOVIE IDs from multiple endpoints
def extract_all_movie_ids(
    pages_popular=5, pages_top=5, pages_upcoming=5, pages_trending=5
):
    logger.info("Fetching all movie lists...")

    popular = fetch_popular_movies(pages_popular)
    top_rated = fetch_top_rated_movies(pages_top)
    upcoming = fetch_upcoming_movies(pages_upcoming)
    trending = fetch_trending_movies(pages_trending)

    all_ids = set(
        [m["id"] for m in popular]
        + [m["id"] for m in top_rated]
        + [m["id"] for m in upcoming]
        + [m["id"] for m in trending]
    )

    logger.info(f"Total unique Movie IDs collected = {len(all_ids)}")
    return list(all_ids)


# STEP 2 — Fetch DETAILS and CREDITS for each movie
def extract_all_categories(movie_ids):
    logger.info("Fetching MOVIE DETAILS + CREDITS for each movie")

    movie_details = []
    movie_credits = []

    # Normal Python loop — tqdm removed  
    for movie_id in movie_ids:
        details = fetch_movie_details(movie_id)
        credits = fetch_movie_credits(movie_id)

        if details:
            movie_details.append(details)
        if credits:
            movie_credits.append(credits)

        # Prevent hitting TMDB rate limit
        time.sleep(0.25)

    return movie_details, movie_credits



