![MIT License](https://img.shields.io/badge/license-MIT-green)
![Build](https://img.shields.io/github/actions/workflow/status/yourname/rss-to-gotify/docker-image.yml)

# RSS to Gotify Notifier

This lightweight service monitors an RSS feed and sends push notifications via Gotify when new entries are detected.

## Features

-   Dockerized and lightweight (based on Python slim)
    or
-   Local via Python3 [view Documentation](LOCAL_SETUP.md)
    <br>
-   Persistent state with a simple JSON file (no database needed)
-   Sends startup ("wakeup") notification
-   Sends notifications on new feed items
-   Error notifications if the RSS feed is unreachable or malformed

## Configuration

Set the following environment variables:

-   `GOTIFY_URL`: Your Gotify server URL (e.g., `https://gotify.example.com`)
-   `APP_TOKEN`: Gotify app token (used to send messages)
-   `RSS_FEED_URL`: URL of the RSS feed to monitor
-   `CHECK_INTERVAL`: Time in seconds between checks (default: 300)

## Run with Docker

In all three approaches, you'll need to set the environment variables.

### Build it yourself

download the repo

```bash
docker build -t rss-via-gotify .
docker run -d \
    -e GOTIFY_URL=https://your-gotify-instance.com \
    -e APP_TOKEN=your_gotify_token \
    -e RSS_FEED_URL=https://example.com/feed \
    -e CHECK_INTERVAL=seconds \
    -v $(pwd)/feed_state.json:/app/feed_state.json \
    rss-via-gotify
```

### Use the available Release

```bash
docker image ##downloawd somehow
docker run -d \
    -e GOTIFY_URL=https://your-gotify-instance.com \
    -e APP_TOKEN=your_gotify_token \
    -e RSS_FEED_URL=https://example.com/feed \
    -e CHECK_INTERVAL=seconds \
    -v where-you-want/feed_state.json:/app/feed_state.json \
    rss-via-gotify
```

### Use Docker-compose

This option can be used in combination with the [Release image](#use-the-available-release) or the [Build it yourself](#build-it-yourself) aproach

```bash
name: <rss-via-gotify>
services:
    rss-via-gotify:
        environment:
            - GOTIFY_URL=https://your-gotify-instance.com
            - APP_TOKEN=your_gotify_token
            - RSS_FEED_URL=https://example.com/feed
            - CHECK_INTERVAL=seconds
        volumes:
            - where-you-want/feed_state.json:/app/feed_state.json
        image: rss-via-gotify
```

## License

MIT
