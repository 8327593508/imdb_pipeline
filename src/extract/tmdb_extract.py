from typing import List, Dict
from config.config import TMDB_API_KEY, MAX_PAGES
from src.utils.session_retry import create_session
from src.utils.logger import get_logger
import time

logger = get_logger('tmdb_extract')

def fetch_popular_pages(max_pages: int = MAX_PAGES) -> List[Dict]:
    """
    Fetches multiple pages of TMDB popular movie data using API v3.
    Returns a list of dictionaries (raw JSON).
    """
    s = create_session()
    all_results = []

    for page in range(1, max_pages + 1):
        url = (
            f"https://api.themoviedb.org/3/movie/popular"
            f"?api_key={TMDB_API_KEY}&language=en-US&page={page}"
        )

        logger.info(f"Fetching TMDB page {page}")

        response = s.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        results = data.get("results", [])

        all_results.extend(results)

        time.sleep(0.2)  # small delay to avoid rate-limit issues

    logger.info(f"Total movies fetched: {len(all_results)}")
    return all_results
