# Local Setup (Without Docker)

If you'd prefer to run this project without Docker, follow these steps:

---

## 🧱 1. Clone the repository

```bash
git clone https://github.com/JKB0DY/rss-via-gotify.git
cd rss-via-gotify
```

---

## 🐍 2. (Optional) Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 📦 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

---

## 🔧 4. Create a `.env` file

This allows you to configure the app without exporting variables every time. Create a file named `.env` in the root directory:

```env
GOTIFY_URL=https://your-gotify-server.com
APP_TOKEN=your_app_token
RSS_FEED_URL=https://example.com/feed
CHECK_INTERVAL=seconds
```

---

## 🚀 5. Run the app

```bash
python main.py
```

---

## 🛠️ 6. Optional: Run persistently

You can use tools like `pm2`, `systemd`, or `supervisord` to keep the script running in the background.

---

## 📝 Notes

-   The app uses `os.getenv()` to read your config.
-   If `.env` is found, it will auto-load (via `python-dotenv`).
-   Make sure to add `.env` to `.gitignore` to keep your secrets safe.
