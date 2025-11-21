# src/load/load_to_postgres.py

from typing import List, Dict

from sqlalchemy import text
from src.utils.db_engine import get_engine
from src.utils.logger import get_logger

logger = get_logger("load")
engine = get_engine()


def _execute_bulk(sql: str, rows: List[Dict]) -> None:
    """Helper to execute a bulk INSERT/UPSERT with a list of dicts."""
    if not rows:
        logger.info("No rows to load, skipping.")
        return

    with engine.begin() as conn:
        conn.execute(text(sql), rows)


def upsert_movies(df_movies):
    """
    Load popular movies into popular_movies table.
    Uses TMDB's 'id' as the primary key (column name: id).
    """
    logger.info(f"Loading {len(df_movies)} popular movies into 'popular_movies'...")

    # IMPORTANT: df_movies must have column 'id', not 'movie_id'
    rows = df_movies.to_dict(orient="records")

    sql = """
        INSERT INTO popular_movies (
            id,
            title,
            vote_average,
            vote_count,
            popularity,
            release_date,
            original_language,
            last_updated
        )
        VALUES (
            :id,
            :title,
            :vote_average,
            :vote_count,
            :popularity,
            :release_date,
            :original_language,
            NOW()
        )
        ON CONFLICT (id) DO UPDATE SET
            title            = EXCLUDED.title,
            vote_average     = EXCLUDED.vote_average,
            vote_count       = EXCLUDED.vote_count,
            popularity       = EXCLUDED.popularity,
            release_date     = EXCLUDED.release_date,
            original_language = EXCLUDED.original_language,
            last_updated     = NOW();
    """

    _execute_bulk(sql, rows)
    logger.info("Upserted popular movies.")


def upsert_movie_details(df_details):
    """
    Load detailed movie info into movie_details table.
    Here the primary key is also 'id'.
    """
    logger.info(f"Loading {len(df_details)} movie details into 'movie_details'...")

    rows = df_details.to_dict(orient="records")

    sql = """
        INSERT INTO movie_details (
            id,
            title,
            overview,
            release_date,
            popularity,
            vote_count,
            vote_average,
            poster_path,
            backdrop_path,
            original_language,
            genres,
            runtime,
            budget,
            revenue,
            homepage,
            tagline,
            status,
            imdb_id,
            production_companies,
            production_countries,
            spoken_languages
        )
        VALUES (
            :id,
            :title,
            :overview,
            :release_date,
            :popularity,
            :vote_count,
            :vote_average,
            :poster_path,
            :backdrop_path,
            :original_language,
            :genres,
            :runtime,
            :budget,
            :revenue,
            :homepage,
            :tagline,
            :status,
            :imdb_id,
            :production_companies,
            :production_countries,
            :spoken_languages
        )
        ON CONFLICT (id) DO UPDATE SET
            title                 = EXCLUDED.title,
            overview              = EXCLUDED.overview,
            release_date          = EXCLUDED.release_date,
            popularity            = EXCLUDED.popularity,
            vote_count            = EXCLUDED.vote_count,
            vote_average          = EXCLUDED.vote_average,
            poster_path           = EXCLUDED.poster_path,
            backdrop_path         = EXCLUDED.backdrop_path,
            original_language     = EXCLUDED.original_language,
            genres                = EXCLUDED.genres,
            runtime               = EXCLUDED.runtime,
            budget                = EXCLUDED.budget,
            revenue               = EXCLUDED.revenue,
            homepage              = EXCLUDED.homepage,
            tagline               = EXCLUDED.tagline,
            status                = EXCLUDED.status,
            imdb_id               = EXCLUDED.imdb_id,
            production_companies  = EXCLUDED.production_companies,
            production_countries  = EXCLUDED.production_countries,
            spoken_languages      = EXCLUDED.spoken_languages;
    """

    _execute_bulk(sql, rows)
    logger.info("Upserted movie details.")


def upsert_movie_credits(df_credits):
    """
    Load cast & crew into movie_credits table.
    Column names must be: movie_id, movie_cast, movie_crew
    """
    logger.info(f"Loading {len(df_credits)} movie credits into 'movie_credits'...")

    rows = df_credits.to_dict(orient="records")

    sql = """
        INSERT INTO movie_credits (
            movie_id,
            movie_cast,
            movie_crew
        )
        VALUES (
            :movie_id,
            :movie_cast,
            :movie_crew
        )
        ON CONFLICT (movie_id) DO UPDATE SET
            movie_cast = EXCLUDED.movie_cast,
            movie_crew = EXCLUDED.movie_crew;
    """

    _execute_bulk(sql, rows)
    logger.info("Upserted movie credits.")
