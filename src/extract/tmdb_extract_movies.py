# src/extract/tmdb_extract_movies.py
import requests
from src.utils.logger import get_logger
from config.config import TMDB_API_KEY

logger = get_logger("tmdb_extract_movies")

BASE_URL = "https://api.themoviedb.org/3"

def fetch_pages(url: str, pages: int):
    """Fetch multiple pages from a TMDB list endpoint and return combined results list."""
    results = []
    for page in range(1, pages + 1):
        logger.info(f"Fetching {url} page {page}...")
        try:
            resp = requests.get(
                url,
                params={"api_key": TMDB_API_KEY, "page": page},
                timeout=10,
            )
        except Exception as e:
            logger.error(f"Request error on {url} page {page}: {e}")
            continue

        if resp.status_code == 200:
            data = resp.json() or {}
            results.extend(data.get("results", []))
        else:
            logger.error(
                f"Failed to fetch {url} page {page} (status {resp.status_code})"
            )
    return results


def fetch_popular_movies(pages: int = 5):
    return fetch_pages(f"{BASE_URL}/movie/popular", pages)

def fetch_top_rated_movies(pages: int = 5):
    return fetch_pages(f"{BASE_URL}/movie/top_rated", pages)

def fetch_upcoming_movies(pages: int = 3):
    return fetch_pages(f"{BASE_URL}/movie/upcoming", pages)

def fetch_trending_movies(pages: int = 3):
    return fetch_pages(f"{BASE_URL}/trending/movie/week", pages)

