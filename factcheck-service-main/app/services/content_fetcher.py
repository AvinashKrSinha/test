# app/services/content_fetcher.py
import requests
from bs4 import BeautifulSoup
import base64
import logging

logger = logging.getLogger("factcheck_service")

def fetch_content_from_url(url: str) -> str:
    """
    Extract text content from a given URL.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        content_type = response.headers.get('Content-Type', '')

        if "text/html" in content_type:
            soup = BeautifulSoup(response.text, "html.parser")
            # Get all paragraph text
            paragraphs = soup.find_all("p")
            text = " ".join([p.get_text() for p in paragraphs])
            return text.strip()
        else:
            logger.warning("URL does not contain HTML content")
            return ""
    except Exception as e:
        logger.error(f"Failed to fetch URL {url}: {e}")
        return ""

def decode_file(file_content_base64: str) -> bytes:
    """
    Decode base64-encoded image/video file.
    """
    try:
        return base64.b64decode(file_content_base64)
    except Exception as e:
        logger.error(f"Failed to decode file content: {e}")
        return b""
