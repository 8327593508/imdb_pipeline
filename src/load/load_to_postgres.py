import pandas as pd
from src.utils.db_engine import get_engine
from src.utils.logger import get_logger
import json

logger = get_logger("load_to_postgres")


def upsert_movies(df_movies):
    """Upsert popular movies into popular_movies table."""
    
    if df_movies.empty:
        logger.warning("No movies to insert")
        return
    
    engine = get_engine()
    conn = engine.raw_connection()
    cursor = conn.cursor()
    
    try:
        for _, movie in df_movies.iterrows():
            movie_id = int(movie.get("id", 0))
            title = movie.get("title", "")
            vote_avg = float(movie.get("vote_average", 0))
            vote_count = int(movie.get("vote_count", 0))
            popularity = float(movie.get("popularity", 0))
            release_date = str(movie.get("release_date", ""))
            language = movie.get("original_language", "en")
            
            values = (
                movie_id,
                title,
                vote_avg,
                vote_count,
                popularity,
                release_date,
                language
            )
            
            cursor.execute("""
                INSERT INTO popular_movies 
                (id, title, vote_average, vote_count, popularity, release_date, original_language)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id)
                DO UPDATE SET
                    title = EXCLUDED.title,
                    vote_average = EXCLUDED.vote_average,
                    vote_count = EXCLUDED.vote_count,
                    popularity = EXCLUDED.popularity,
                    release_date = EXCLUDED.release_date,
                    original_language = EXCLUDED.original_language,
                    last_updated = CURRENT_TIMESTAMP;
            """, values)
        
        conn.commit()
        logger.info(f"Successfully inserted {len(df_movies)} movies")
        
    except Exception as e:
        logger.error(f"Error inserting movies: {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
