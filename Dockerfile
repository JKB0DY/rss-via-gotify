FROM python:3.11-slim

WORKDIR /app

COPY requirements_docker.txt ./
RUN pip install --no-cache-dir -r requirements_docker.txt

COPY ../main.py ./

LABEL org.opencontainers.image.source=https://github.com/JKB0DY/rss-via-gotify
LABEL org.opencontainers.image.description="A simple RSS feed reader that sends notifications to Gotify."
LABEL org.opencontainers.image.licenses=MIT

CMD ["python", "main.py"]