import logging
import requests
from typing import Optional

logger = logging.getLogger(__name__)

def send_request(roku_ip: str, path: str, params: Optional[dict] = None, method: str = "GET") -> str:
    """
    Send a request to a Roku device and return raw response text.
    """
    url = f"http://{roku_ip}:8060/{path.lstrip('/')}"
    if method.upper() == "POST":
        resp = requests.post(url, params=params or {}, data="", timeout=5)
    else:
        resp = requests.get(url, params=params, timeout=5)
    try:
        resp.raise_for_status()
        return resp.text
    except requests.HTTPError as e:
        if resp.status_code == 404:
            logger.error(f"URL not found: {url}")
        elif resp.status_code == 403:
            logger.error(f"Forbidden: Roku may be in Limited mode ({url})")
        else:
            logger.error(f"HTTP error {resp.status_code}: {e}")
        return ""
    except requests.RequestException as e:
        logger.exception(f"Request failed: {e}")
        return ""
