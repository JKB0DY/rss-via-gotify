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

def load_state():
    """Load the last known feed entry ID from the state file."""
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        send_notification("Warning", "Could not decode state file, starting fresh.")
        return {}

def save_state(state):
    """Save the current state to a file."""
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(state, f)
    except Exception as e:
        send_notification("Error saving state", str(e))

def send_notification(title, message, priority=5):
    """Send a push notification to Gotify."""
    try:
        response = requests.post(
            f"{GOTIFY_URL}/message?token={APP_TOKEN}",
            json={"title": title, "message": message, "priority": priority}
        )
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to send notification: {e}")

def check_feed(last_id):
    """Check the RSS feed and return a new ID if there's a new entry."""
    try:
        feed = feedparser.parse(RSS_FEED_URL, agent=USER_AGENT)

        # Check for parsing errors or bad status
        if feed.bozo:
            raise Exception(f"Feed parsing failed: {feed.bozo_exception}")

        if not feed.entries:
            return last_id  # Nothing to do

        latest = feed.entries[0]
        entry_id = latest.get("id", latest.get("guid"))

        if entry_id != last_id:
            title = latest.get("title", "New RSS Entry")
            link = latest.get("link", "")
            summary = latest.get("summary", "")
            if summary != "Summary:":
                send_notification(title, f"{summary}\n{link}")
            else:
                send_notification("Exam Notification", link , priority=4)
            return entry_id

        return last_id

    except Exception as e:
        send_notification("RSS Feed Error", f"Could not read feed: {e}", priority=4)
        return last_id

def main():
    # Load previous state
    state = load_state()
    last_id = state.get("last_id")

    # Wakeup notification
    send_notification(
        "RSS Monitor Started",
        f"Monitoring: {RSS_FEED_URL}\nInterval: {CHECK_INTERVAL}s",
        priority=3
    )

    while True:
        try:
            new_id = check_feed(last_id)

            if new_id != last_id:
                last_id = new_id
                save_state({"last_id": last_id})

        except Exception as e:
            send_notification("Unexpected Error", str(e), priority=4)

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()