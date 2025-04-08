import time
import feedparser
import requests
import json
import os

# Load .env only if running outside Docker
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Dotenv is optional, ignore if not installed

# Configuration via environment variables
GOTIFY_URL = os.getenv("GOTIFY_URL")
APP_TOKEN = os.getenv("APP_TOKEN")
RSS_FEED_URL = os.getenv("RSS_FEED_URL")
USER_AGENT = os.getenv("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 300))
STATE_FILE = "feed_state.json"


def fetch_feed():
    try:
        feed = feedparser.parse(RSS_FEED_URL, agent=USER_AGENT)

        if feed.bozo:
            raise Exception(f"Feed parsing error: {feed.bozo_exception}")

    except Exception as e:
        print(feed.headers)
        feed = None

    return feed

fetch_feed()