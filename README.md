# comics-rss-feed

Parse comics page to generate rss feed. Filter feeds by favorite/ignore so only favorite feeds are parsed.

## How to run

Required env variables:
- RSS_URL - Tiny Tiny RSS URL
- RSS_LOGIN - Tiny Tiny RSS user
- RSS_PASSWORD - Tiny Tiny RSS user password
- XML_FOLDER - Directory to store the generated feeds
- RSS_SCRAPPER_URL - Where the generated feeds will be served -> must be reachable by the RSS server
- COMICS_DEFAULT_FEED_CATEGORY_TITLE - New feeds get added to this category. Default: _GoComics_
- COMICS_FAVORITE_FEED_CATEGORY_TITLE - Favorite feeds category. Default: _GoComics-always_

# Ignore feeds in this category 
COMICS_IGNORE_FEED_CATEGORY_TITLE = os.getenv('COMICS_IGNORE_FEED_CATEGORY_TITLE', "GoComics-ignore")

## Prereqs to build

You need to create the following secrets (not needed within the k8s-at-home org - there we use org-wide secrets):
- WORKFLOW_REPO_SYNC_TOKEN # Needed to do PRs that update the workflows
- GHCR_USERNAME # Needed to upload container to the Github Container Registry
- GHCR_TOKEN # Needed to upload container to the Github Container Registry

## How to build

2. Build the container
    ```bash
    make
    ```

Check the [Makefile] for other build targets


