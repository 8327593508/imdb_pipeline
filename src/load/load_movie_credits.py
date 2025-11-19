from src.utils.db_engine import get_engine

def load_movie_credits(df):
    engine = get_engine()
    df.to_sql("movie_credits", engine, if_exists="replace", index=False)
