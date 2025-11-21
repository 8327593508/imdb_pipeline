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
from config.config import MAX_PAGES
import time

logger = get_logger("tmdb_master_extract")


def extract_all_categories(
    pages_popular: int | None = None,
    pages_top: int | None = None,
    pages_upcoming: int | None = None,
    pages_trending: int | None = None,
):
    """Fetch movies from multiple TMDB list endpoints + details + credits.

    Returns a dict with:
      - popular: list[dict]
      - top_rated: list[dict]
      - upcoming: list[dict]
      - trending: list[dict]
      - details: list[dict]
      - credits: list[dict] with keys movie_id, cast, crew
    """

    if pages_popular is None:
        pages_popular = MAX_PAGES
    if pages_top is None:
        pages_top = MAX_PAGES
    if pages_upcoming is None:
        pages_upcoming = 3
    if pages_trending is None:
        pages_trending = 3

    logger.info("Fetching category movie lists...")

    popular = fetch_popular_movies(pages_popular)
    top_rated = fetch_top_rated_movies(pages_top)
    upcoming = fetch_upcoming_movies(pages_upcoming)
    trending = fetch_trending_movies(pages_trending)

    # Build set of unique IDs across all categories
    movie_ids = set()
    for m in popular:
        movie_ids.add(m.get("id"))
    for m in top_rated:
        movie_ids.add(m.get("id"))
    for m in upcoming:
        movie_ids.add(m.get("id"))
    for m in trending:
        movie_ids.add(m.get("id"))

    movie_ids.discard(None)
    logger.info(f"Total unique movie IDs collected: {len(movie_ids)}")

    details_list: list[dict] = []
    credits_list: list[dict] = []

    logger.info("Fetching details + credits for each movie...")

    for movie_id in movie_ids:
        # Details
        d = fetch_movie_details(movie_id)
        if d:
            details_list.append(d)

        # Credits
        c = fetch_movie_credits(movie_id)
        if c:
            credits_list.append(
                {
                    "movie_id": movie_id,
                    "cast": c.get("cast"),
                    "crew": c.get("crew"),
                }
            )

        # Be gentle with TMDB API
        time.sleep(0.25)

    return {
        "popular": popular,
        "top_rated": top_rated,
        "upcoming": upcoming,
        "trending": trending,
        "details": details_list,
        "credits": credits_list,
    }






