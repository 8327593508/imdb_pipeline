import requests
from src.utils.logger import get_logger
from config.config import TMDB_API_KEY
from src.utils.session_retry import create_retry_session

logger = get_logger("tmdb_extract_credits")

BASE_URL = "https://api.themoviedb.org/3/movie/{movie_id}/credits"


def extract_movie_credits(movie_id: int):
    """Fetch cast and crew for a movie."""
    url = BASE_URL.format(movie_id=movie_id)
    params = {"api_key": TMDB_API_KEY}

      session = create_retry_session()

    logger.info(f"Fetching credits for movie_id={movie_id}")
    response = session.get(url, params=params)

    if response.status_code != 200:
        logger.error(f"Failed to fetch credits for movie {movie_id}")
        return None

    data = response.json()

    return {
        "movie_id": movie_id,
        "movie_cast": data.get("cast", []),   # UPDATED
        "movie_crew": data.get("crew", [])    # UPDATED
    }


def extract_all_movie_credits(movie_ids: list[int]):
    """Extract credits for all movie IDs."""
    all_rows = []

    for movie_id in movie_ids:
        result = extract_movie_credits(movie_id)
        if result:
            all_rows.append(result)

    return all_rows

