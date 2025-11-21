import pandas as pd
from src.utils.db_engine import engine

def upsert_movie_details(df: pd.DataFrame):
    df.to_sql("movie_details", engine, if_exists="append", index=False)

