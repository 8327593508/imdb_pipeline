# src/extract/tmdb_master_extract.py
from src.extract.tmdb_extract_movies import (
    fetch_popular_movies,
    fetch_top_rated_movies,
    fetch_upcoming_movies,
    fetch_trending_movies,
)
from src.extract.tmdb_extract_details import fetch_movie_details
from src.extract.tmdb_extract_credits import fetch_movie_credits
from src.utils.logger import get_logger
import time

logger = get_logger("tmdb_master_extract")


def extract_all_categories(pages=50):
    logger.info("Fetching popular movies...")
    popular = fetch_popular_movies(pages)

    logger.info("Fetching top rated movies...")
    top_rated = fetch_top_rated_movies(pages)

    logger.info("Fetching upcoming movies...")
    upcoming = fetch_upcoming_movies(pages)

    logger.info("Fetching trending movies...")
    trending = fetch_trending_movies(pages)

    # Combine
    all_basic = popular + top_rated + upcoming + trending

    # Extract only IDs
    movie_ids = list({m["id"] for m in all_basic})
    logger.info(f"Total unique movie IDs collected: {len(movie_ids)}")

    # Fetch details + credits
    details = []
    credits = []

    for movie_id in movie_ids:
        d = fetch_movie_details(movie_id)
        if d:
            details.append(d)

        c = fetch_movie_credits(movie_id)
        if c:
            credits.append({"movie_id": movie_id, **c})

    return popular, top_rated, upcoming, trending, details, credits




