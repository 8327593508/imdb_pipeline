from dotenv import load_dotenv
import os
from pathlib import Path

# Load .env file from project root
ROOT = Path(__file__).resolve().parents[1]
load_dotenv(dotenv_path=ROOT / '.env')

# TMDB Settings
TMDB_API_KEY = os.getenv('TMDB_API_KEY')

# PostgreSQL Settings
PG_USER = os.getenv('PG_USER', 'postgres')
PG_PASSWORD = os.getenv('PG_PASSWORD', '')
PG_HOST = os.getenv('PG_HOST', 'localhost')
PG_DB = os.getenv('PG_DB', 'tmdb_db')
PG_PORT = os.getenv('PG_PORT', '5432')

# Pipeline Settings
MAX_PAGES = int(os.getenv('MAX_PAGES', '5'))
SCHEDULE = os.getenv('SCHEDULE')  # seconds or empty
