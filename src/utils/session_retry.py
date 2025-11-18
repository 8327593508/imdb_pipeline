import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session(total_retries: int = 5, backoff: float = 0.5) -> requests.Session:
    s = requests.Session()
    retries = Retry(
        total=total_retries,
        backoff_factor=backoff,
        status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retries)
    s.mount('https://', adapter)
    s.mount('http://', adapter)
    return s
