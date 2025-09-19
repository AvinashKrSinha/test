import os
import json
import requests
from google.cloud import storage
from datetime import datetime, timezone


GCS_BUCKET = os.environ.get("GCS_BUCKET")
TRUSTED_SOURCES = [
    "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"
]

storage_client = storage.Client()

def fetch_articles(request):
    all_articles = []

    for url in TRUSTED_SOURCES:
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                all_articles.append({
                    "source": url,
                    "content": resp.text
                })
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")

    # Save to GCS
    if all_articles:
        bucket = storage_client.bucket(GCS_BUCKET)
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H-%M-%S")
        blob = bucket.blob(f"{timestamp}.json")
        blob.upload_from_string(json.dumps(all_articles), content_type="application/json")
        return f"Saved {len(all_articles)} articles to GCS at {timestamp}"
    else:
        return "No articles fetched"
