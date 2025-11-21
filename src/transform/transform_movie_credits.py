import pandas as pd

def transform_movie_credits(credits_list):
    formatted = []

    for row in credits_list:
        formatted.append({
            "movie_id": row.get("id"),
            "cast": row.get("cast"),
            "crew": row.get("crew")
        })

    return pd.DataFrame(formatted)

