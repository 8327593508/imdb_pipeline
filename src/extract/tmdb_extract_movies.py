# src/extract/tmdb_extract_movies.py
import requests
from src.utils.logger import get_logger
from config.config import TMDB_API_KEY

logger = get_logger("tmdb_extract_movies")

BASE_URL = "https://api.themoviedb.org/3"

def fetch_pages(url, pages):
    results = []
    for page in range(1, pages + 1):
        logger.info(f"Fetching {url} page {page}...")
        r = requests.get(f"{url}?api_key={TMDB_API_KEY}&page={page}")
        if r.status_code == 200:
            results.extend(r.json().get("results", []))
        else:
            logger.error(f"Error {r.status_code} fetching page {page}")
    return results


def fetch_popular_movies(pages=100):
    return fetch_pages(f"{BASE_URL}/movie/popular", pages)

def fetch_top_rated_movies(pages=100):
    return fetch_pages(f"{BASE_URL}/movie/top_rated", pages)

def fetch_upcoming_movies(pages=50):
    return fetch_pages(f"{BASE_URL}/movie/upcoming", pages)

def fetch_trending_movies(pages=50):
    return fetch_pages(f"{BASE_URL}/trending/movie/week", pages)
