import json
from src.utils.db_engine import get_engine
from src.utils.logger import get_logger

logger = get_logger("load_movie_details")


def upsert_movie_details(df_details):
    """Upsert movie details into movie_details table."""
    
    if df_details.empty:
        logger.warning("No details to insert")
        return
    
    engine = get_engine()
    conn = engine.raw_connection()
    cursor = conn.cursor()
    
    try:
        for _, row in df_details.iterrows():
            movie_id = int(row.get("id", 0))
            title = row.get("title", "")
            overview = row.get("overview", "")
            release_date = str(row.get("release_date", ""))
            popularity = float(row.get("popularity", 0))
            vote_count = int(row.get("vote_count", 0))
            vote_avg = float(row.get("vote_average", 0))
            poster_path = row.get("poster_path")
            backdrop_path = row.get("backdrop_path")
            language = row.get("original_language", "en")
            genres = json.dumps(row.get("genres", []))
            runtime = int(row.get("runtime", 0)) if row.get("runtime") else None
            budget = int(row.get("budget", 0)) if row.get("budget") else 0
            revenue = int(row.get("revenue", 0)) if row.get("revenue") else 0
            homepage = row.get("homepage")
            tagline = row.get("tagline")
            status = row.get("status")
            imdb_id = row.get("imdb_id")
            prod_companies = json.dumps(row.get("production_companies", []))
            prod_countries = json.dumps(row.get("production_countries", []))
            spoken_langs = json.dumps(row.get("spoken_languages", []))
            
            cursor.execute("""
                INSERT INTO movie_details 
                (id, title, overview, release_date, popularity, vote_count, vote_average,
                 poster_path, backdrop_path, original_language, genres, runtime, budget, revenue,
                 homepage, tagline, status, imdb_id, production_companies, production_countries, spoken_languages)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id)
                DO UPDATE SET
                    overview = EXCLUDED.overview,
                    genres = EXCLUDED.genres,
                    runtime = EXCLUDED.runtime,
                    budget = EXCLUDED.budget,
                    revenue = EXCLUDED.revenue,
                    last_updated = CURRENT_TIMESTAMP;
            """, (
                movie_id, title, overview, release_date, popularity, vote_count, vote_avg,
                poster_path, backdrop_path, language, genres, runtime, budget, revenue,
                homepage, tagline, status, imdb_id, prod_companies, prod_countries, spoken_langs
            ))
        
        conn.commit()
        logger.info(f"Successfully inserted {len(df_details)} movie details")
        
    except Exception as e:
        logger.error(f"Error inserting movie details: {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
