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
from tqdm import tqdm  # progress bar

logger = get_logger("tmdb_master_extract")


def extract_all_categories(
    pages_popular=200,
    pages_top=200,
    pages_upcoming=50,
    pages_trending=50
):
    """
    Extracts movie IDs from 4 TMDB categories:
        - Popular
        - Top Rated
        - Upcoming
        - Trending

    Then fetches FULL details + credits for each movie and returns:
        movies_details, movies_credits
    """

    logger.info("Fetching movie lists from TMDB...")

    # FETCH MOVIE LISTS
    popular = fetch_popular_movies(pages_popular)
    top_rated = fetch_top_rated_movies(pages_top)
    upcoming = fetch_upcoming_movies(pages_upcoming)
    trending = fetch_trending_movies(pages_trending)

    logger.info("Collecting movie IDs from all categories...")

    # Extract movie IDs
    all_ids = set()

    for row in (popular + top_rated + upcoming + trending):
        if "id" in row:
            all_ids.add(row["id"])

    logger.info(f"Total unique movie IDs found: {len(all_ids)}")

    movies_details = []
    movies_credits = []

    logger.info("Fetching FULL details + credits for each movie...")

    # Fetch full metadata
    for movie_id in tqdm(all_ids, desc="Processing movie"):
        details = fetch_movie_details(movie_id)
        credits = fetch_movie_credits(movie_id)

        if details:
            movies_details.append(details)

        if credits:
            movies_credits.append(credits)

        # small delay to avoid rate limiting
        time.sleep(0.15)

    logger.info(
        f"Extracted details: {len(movies_details)} | credits: {len(movies_credits)}"
    )

    return movies_details, movies_credits


