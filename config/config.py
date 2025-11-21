import os
from dotenv import load_dotenv

# Load .env file inside Docker container
load_dotenv()


# -------- Helper Functions -------- #

def get_str_env(name: str, default: str = "") -> str:
    """
    Safely retrieve a string environment variable.
    If not present or empty, return default.
    """
    value = os.getenv(name, "").strip()
    return value if value else default


def get_int_env(name: str, default: int = 0) -> int:
    """
    Safely retrieve an integer environment variable.
    If conversion fails or missing, return default.
    """
    value = os.getenv(name, "").strip()
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


# -------- TMDB API Keys -------- #
TMDB_API_KEY = get_str_env("TMDB_API_KEY", "")

# You may use different keys later if needed:
TMDB_API_POPULAR = get_str_env("TMDB_API_POPULAR", TMDB_API_KEY)
TMDB_API_TOP = get_str_env("TMDB_API_TOP", TMDB_API_KEY)


# -------- PostgreSQL Credentials -------- #
PG_USER = get_str_env("PG_USER", "postgres")
PG_PASSWORD = get_str_env("PG_PASSWORD", "")
PG_DB = get_str_env("PG_DB", "tmdb")
PG_PORT = get_int_env("PG_PORT", 5432)


# -------- Extract Settings -------- #

# Default to 5 pages if environment variable missing
MAX_PAGES = get_int_env("MAX_PAGES", 5)

# Schedule used only if your code references it
SCHEDULE = get_str_env("SCHEDULE", "0 6 * * *")

