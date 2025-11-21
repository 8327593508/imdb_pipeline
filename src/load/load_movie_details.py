import pandas as pd
from src.utils.db_engine import get_engine
engine = get_engine()

def upsert_movie_details(df: pd.DataFrame):
    df.to_sql("movie_details", engine, if_exists="append", index=False)

