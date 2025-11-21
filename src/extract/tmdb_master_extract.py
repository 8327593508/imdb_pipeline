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


def extract_all_categories(
    pages_popular=5,
    pages_top=5,
    pages_upcoming=3,
    pages_trending=3
):
    logger.info("Fetching category movie lists...")

    popular = fetch_popular_movies(pages_popular)
    top_rated = fetch_top_rated_movies(pages_top)
    upcoming = fetch_upcoming_movies(pages_upcoming)
    trending = fetch_trending_movies(pages_trending)

    movie_ids = set()

    # Add movie IDs for each category
    for m in popular:
        movie_ids.add(m["id"])
    for m in top_rated:
        movie_ids.add(m["id"])
    for m in upcoming:
        movie_ids.add(m["id"])
    for m in trending:
        movie_ids.add(m["id"])

    logger.info(f"Total unique movie IDs collected: {len(movie_ids)}")

    details_list = []
    credits_list = []

    logger.info("Downloading details + credits for each movie...")

    for movie_id in movie_ids:
        d = fetch_movie_details(movie_id)
        c = fetch_movie_credits(movie_id)

        if d:
            details_list.append(d)
        if c:
            credits_list.append({"movie_id": movie_id, "cast": c["cast"], "crew": c["crew"]})

        time.sleep(0.25)  # avoid rate limit

    return {
        "popular": popular,
        "top_rated": top_rated,
        "upcoming": upcoming,
        "trending": trending,
        "details": details_list,
        "credits": credits_list,
    }





