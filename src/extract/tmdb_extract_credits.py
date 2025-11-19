# src/extract/tmdb_extract_credits.py
import requests
from src.utils.logger import get_logger
from config.config import TMDB_API_KEY

logger = get_logger("tmdb_extract_credits")

BASE_URL = "https://api.themoviedb.org/3/movie"

def fetch_movie_credits(movie_id):
    """
    Fetch cast and crew details for a movie.
    """
    url = f"{BASE_URL}/{movie_id}/credits?api_key={TMDB_API_KEY}"

    logger.info(f"Fetching credits for movie ID {movie_id}...")

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()

    else:
        logger.error(
            f"Failed to fetch credits for ID {movie_id} (Status {response.status_code})"
        )
        return None
