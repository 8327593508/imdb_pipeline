import pandas as pd
from src.utils.db_engine import engine

def upsert_movie_credits(df: pd.DataFrame):
    df.to_sql("movie_credits", engine, if_exists="append", index=False)

