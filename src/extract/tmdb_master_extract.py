# src/extract/tmdb_master_extract.py
from src.extract.tmdb_extract_movies import (
    fetch_popular_movies,
    fetch_top_rated_movies,
    fetch_upcoming_movies,
    fetch_trending_movies
)
from src.extract.tmdb_extract_details import fetch_movie_details
from src.extract.tmdb_extract_credits import fetch_movie_credits
from src.utils.logger import get_logger
from tqdm import tqdm
import pandas as pd
import time

logger = get_logger("tmdb_master_extract")


def enrich_movie_list(movie_list, label="dataset"):
    """
    Takes a list of {'id': movie_id} dicts
    Fetches full details + credits for each ID
    Returns a DataFrame
    """
    enriched_rows = []

    logger.info(f"Enriching movies for: {label}. Total IDs = {len(movie_list)}")

    for m in tqdm(movie_list):
        movie_id = m.get("id")

        # Fetch details
        details = fetch_movie_details(movie_id)
        time.sleep(0.25)  # to avoid rate limit

        # Fetch credits
        credits = fetch_movie_credits(movie_id)
        time.sleep(0.25)

        if details:
            row = {
                "movie_id": movie_id,
                "title": details.get("title"),
                "overview": details.get("overview"),
                "release_date": details.get("release_date"),
                "runtime": details.get("runtime"),
                "genres": [g["name"] for g in details.get("genres", [])],
                "vote_average": details.get("vote_average"),
                "vote_count": details.get("vote_count"),
                "popularity": details.get("popularity"),
                "poster_path": details.get("poster_path"),
                "backdrop_path": details.get("backdrop_path"),
                "cast": credits.get("cast", []) if credits else [],
                "crew": credits.get("crew", []) if credits else [],
            }

            enriched_rows.append(row)

    df = pd.DataFrame(enriched_rows)
    logger.info(f"Finished enriching: {label}. Final rows = {len(df)}")

    return df


def extract_all_categories(
    pages_popular=200, pages_top=200, pages_upcoming=50, pages_trending=50
):
    """
    Fetch movie ID lists for all 4 collections
    Then enrich each list with details + credits
    Then return 4 DataFrames
    """

    logger.info("Fetching movie ID lists...")

    popular_ids = fetch_popular_movies(pages_popular)
    top_ids = fetch_top_rated_movies(pages_top)
    upcoming_ids = fetch_upcoming_movies(pages_upcoming)
    trending_ids = fetch_trending_movies(pages_trending)

    logger.info(
        f"ID counts → Popular: {len(popular_ids)}, Top: {len(top_ids)}, "
        f"Upcoming: {len(upcoming_ids)}, Trending: {len(trending_ids)}"
    )

    # Now enrich each category
    df_popular = enrich_movie_list(popular_ids, "popular")
    df_top = enrich_movie_list(top_ids, "top_rated")
    df_upcoming = enrich_movie_list(upcoming_ids, "upcoming")
    df_trending = enrich_movie_list(trending_ids, "trending")

    return df_popular, df_top, df_upcoming, df_trending

