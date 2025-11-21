import pandas as pd
from src.utils.logger import get_logger

logger = get_logger("transform_movie_credits")


def transform_movie_credits(raw_rows: list[dict]):
    """Convert raw credits into DataFrame ready for DB insertion."""
    
    if not raw_rows:
        logger.warning("No credit rows to transform")
        return pd.DataFrame()
    
    transformed = []
    
    for row in raw_rows:
        transformed.append({
            "movie_id": row.get("movie_id"),
            "movie_cast": row.get("movie_cast", []),
            "movie_crew": row.get("movie_crew", [])
        })
    
    df = pd.DataFrame(transformed)
    logger.info(f"Transformed {len(df)} credit rows")
    return df
