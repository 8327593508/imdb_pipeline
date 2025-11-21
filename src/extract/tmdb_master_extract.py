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
        pages_upcoming = 2
    if pages_trending is None:
        pages_trending = 2

    logger.info("Fetching movie lists from TMDB...")

    # Fetch paginated results
    popular = []
    top_rated = []
    upcoming = []
    trending = []

    for page in range(1, pages_popular + 1):
        logger.info(f"Fetching popular movies page {page}/{pages_popular}")
        popular.extend(fetch_popular_movies(page))
        time.sleep(0.25)

    for page in range(1, pages_top + 1):
        logger.info(f"Fetching top_rated movies page {page}/{pages_top}")
        top_rated.extend(fetch_top_rated_movies(page))
        time.sleep(0.25)

    for page in range(1, pages_upcoming + 1):
        logger.info(f"Fetching upcoming movies page {page}/{pages_upcoming}")
        upcoming.extend(fetch_upcoming_movies(page))
        time.sleep(0.25)

    for page in range(1, pages_trending + 1):
        logger.info(f"Fetching trending movies page {page}/{pages_trending}")
        trending.extend(fetch_trending_movies(page))
        time.sleep(0.25)

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

    logger.info(f"Fetching details + credits for {len(movie_ids)} movies...")

    count = 0
    for movie_id in movie_ids:
        count += 1
        if count % 50 == 0:
            logger.info(f"Progress: {count}/{len(movie_ids)}")

        # Details
        d = fetch_movie_details(movie_id)
        if d:
            details_list.append(d)

        # Credits
        c = fetch_movie_credits(movie_id)
        if c:
            credits_list.append(c)

        # Be gentle with TMDB API
        time.sleep(0.25)

    logger.info("Movie extraction completed!")

    return {
        "popular": popular,
        "top_rated": top_rated,
        "upcoming": upcoming,
        "trending": trending,
        "details": details_list,
        "credits": credits_list,
    }





