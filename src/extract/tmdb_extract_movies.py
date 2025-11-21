import requests
from config.config import TMDB_API_KEY, MAX_PAGES
from src.utils.logger import get_logger
from src.utils.session_retry import create_retry_session

logger = get_logger("tmdb_extract_movies")

BASE_URL = "https://api.themoviedb.org/3/movie"


def fetch_popular_movies(page: int):
    """Fetch popular movies from TMDB (1 page)."""

    session = create_retry_session()
    url = f"{BASE_URL}/popular"
    params = {
        "api_key": TMDB_API_KEY,
        "page": page
    }

    response = session.get(url, params=params, timeout=20)
    response.raise_for_status()
    data = response.json()

    if "results" not in data:
        logger.error(f"No 'results' key in response for page {page}")
        return []

    logger.info(f"Fetched {len(data['results'])} movies from page {page}")
    return data["results"]


def fetch_top_rated_movies(page: int):
    """Fetch top-rated movies."""
    session = create_retry_session()
    url = f"{BASE_URL}/top_rated"

    params = {
        "api_key": TMDB_API_KEY,
        "page": page
    }

    response = session.get(url, params=params, timeout=20)
    response.raise_for_status()

    data = response.json()
    return data.get("results", [])


def fetch_trending_movies(page: int):
    """Fetch trending movies."""
    session = create_retry_session()
    url = "https://api.themoviedb.org/3/trending/movie/day"

    params = {
        "api_key": TMDB_API_KEY,
        "page": page
    }

    response = session.get(url, params=params, timeout=20)
    response.raise_for_status()

    data = response.json()
    return data.get("results", [])


def fetch_upcoming_movies(page: int):
    """Fetch upcoming movies."""
    session = create_retry_session()
    url = f"{BASE_URL}/upcoming"

    params = {
        "api_key": TMDB_API_KEY,
        "page": page
    }

    response = session.get(url, params=params, timeout=20)
    response.raise_for_status()

    data = response.json()
    return data.get("results", [])


def extract_all_movie_categories():
    """Extract multiple movie categories over multiple pages."""
    all_movies = {
        "popular": [],
        "top_rated": [],
        "trending": [],
        "upcoming": []
    }

    logger.info(f"Extracting movies — MAX_PAGES = {MAX_PAGES}")

    for page in range(1, MAX_PAGES + 1):
        logger.info(f"Fetching page {page}/{MAX_PAGES}")

        # Each category
        all_movies["popular"] += fetch_popular_movies(page)
        all_movies["top_rated"] += fetch_top_rated_movies(page)
        all_movies["trending"] += fetch_trending_movies(page)
        all_movies["upcoming"] += fetch_upcoming_movies(page)

    logger.info("Movie extraction completed successfully!")
    return all_movies


