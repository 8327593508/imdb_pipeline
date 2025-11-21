import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def create_retry_session():
    """
    Creates a session with retry logic for HTTP requests.
    """
    session = requests.Session()

    retry_strategy = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session

