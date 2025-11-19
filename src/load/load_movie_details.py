from src.utils.db_engine import get_engine

def load_movie_details(df):
    engine = get_engine()
    df.to_sql("movie_details", engine, if_exists="replace", index=False)
