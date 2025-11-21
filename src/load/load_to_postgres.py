import pandas as pd
from src.utils.db_engine import engine

def upsert_movies(df: pd.DataFrame):
    df.to_sql("popular_movies", engine, if_exists="append", index=False)

