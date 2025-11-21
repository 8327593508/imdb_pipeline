from src.utils.logger import get_logger

logger = get_logger("transform_movie_credits")


def transform_movie_credits(raw_rows: list[dict]):
    """Convert raw credits into DB-ready rows."""

    transformed = []

    for row in raw_rows:
        transformed.append({
            "movie_id": row["movie_id"],
            "movie_cast": row.get("movie_cast", []),   # UPDATED
            "movie_crew": row.get("movie_crew", [])    # UPDATED
        })

    logger.info(f"Transformed {len(transformed)} credit rows")
    return transformed


