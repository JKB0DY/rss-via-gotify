import time
import feedparser
import requests
import json
import os

# # Load .env only if running outside Docker
# try:
#     from dotenv import load_dotenv
#     load_dotenv()
# except ImportError:
#     pass  # Dotenv is optional, ignore if not installed

# Configuration via environment variables
RSS_FEED_URL = "https://hisinone.unibw.de/qisserver/pages/cs/sys/portal/feed/portalMessagesFeed.faces?user=c9c69400-5df1-11ee-98a9-ffd59f8f8445c9c69400-5df1-11ee-98a9-ffd59f8f8445&hash=bf000ea22fcdc237b4fe102822e53b23"
CHECK_INTERVAL = 300
STATE_FILE = "feed_state.json"
USER_AGENT = os.getenv("USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36")

feed = feedparser.parse(RSS_FEED_URL, agent=USER_AGENT)
if feed.bozo:
    raise Exception(f"Feed parsing failed: {feed.bozo_exception}")

if not feed.entries:
    # Nothing to do
    print("No new entries in the feed.")
    exit(0)

latest = feed.entries[0]
entry_id = latest.get("id", latest.get("guid"))

if entry_id != 0:
    title = latest.get("title", "New RSS Entry")
    link = latest.get("link", "")
    summary = latest.get("summary", "")
    if link != "https://hisinone.unibw.de:443/qisserver/pages/sul/examAssessment/personExamsReadonly.xhtml?_flowId=examsOverviewForPerson-flow":
        print("New entry found!")
        print(f"Title: {title}")
        print(f"Link: {link}")
        print(f"Summary: {summary}")
    else:
        print("examAssessment entry found.")
        print(f"Title: {title}")
        print(f"Link: {link}")
        print(f"Summary: {summary}")
    try:
        with open(STATE_FILE, "w") as f:
            json.dump({"last_id": entry_id}, f)
    except Exception as e:
        print(f"Failed to save state: {e}")
else:
    print("No new entries.")


