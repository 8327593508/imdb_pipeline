# src/extract/tmdb_extract_details.py
import requests
from src.utils.logger import get_logger
from config.config import TMDB_API_KEY

logger = get_logger("tmdb_extract_details")

BASE_URL = "https://api.themoviedb.org/3/movie"

def fetch_movie_details(movie_id):
    """
    Fetch full details for a single movie.
    """
    url = f"{BASE_URL}/{movie_id}?api_key={TMDB_API_KEY}"

    logger.info(f"Fetching details for movie ID {movie_id}...")

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()

    else:
        logger.error(
            f"Failed to fetch details for ID {movie_id} (Status {response.status_code})"
        )
        return None
