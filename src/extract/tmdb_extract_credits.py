import requests
from src.utils.logger import get_logger
from config.config import TMDB_API_KEY
from src.utils.session_retry import create_retry_session

logger = get_logger("tmdb_extract_credits")

BASE_URL = "https://api.themoviedb.org/3/movie/{movie_id}/credits"

session = create_retry_session()


def fetch_movie_credits(movie_id: int):
    """
    Fetch cast and crew for a movie (single movie credits).
    This matches what main.py imports.
    """
    url = BASE_URL.format(movie_id=movie_id)
    params = {"api_key": TMDB_API_KEY}

    logger.info(f"Fetching credits for movie_id={movie_id}")
    response = session.get(url, params=params)

    if response.status_code != 200:
        logger.error(f"Failed to fetch credits for movie {movie_id} (HTTP {response.status_code})")
        return None

    data = response.json()

    return {
        "movie_id": movie_id,
        "movie_cast": data.get("cast", []),   # JSONB in DB
        "movie_crew": data.get("crew", [])    # JSONB in DB
    }


def fetch_all_movie_credits(movie_ids: list[int]):
    """
    Fetch credits for all movie IDs.
    This replaces extract_all_movie_credits for consistency.
    """
    rows = []

    for movie_id in movie_ids:
        result = fetch_movie_credits(movie_id)
        if result:
            rows.append(result)

    return rows
