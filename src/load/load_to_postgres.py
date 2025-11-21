import pandas as pd
from src.utils.db_engine import get_engine

def upsert_movies(df: pd.DataFrame):
    engine=get_engine()
    df.to_sql("popular_movies", engine, if_exists="append", index=False)

