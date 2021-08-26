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
- COMICS_IGNORE_FEED_CATEGORY_TITLE - Ignore feeds in this category. Default: _GoComics-ignore_

## Prereqs to build

You need to create the following secrets (not needed within the k8s-at-home org - there we use org-wide secrets):
- WORKFLOW_REPO_SYNC_TOKEN # Needed to do PRs that update the workflows
- GHCR_USERNAME # Needed to upload container to the Github Container Registry
- GHCR_TOKEN # Needed to upload container to the Github Container Registry

## How to develop

### Local

1. Create an `envfile` to set the required env variables. It should look like this:
   ```bash
   RSS_URL=https://rss.example.com/api/
   RSS_LOGIN=user
   RSS_PASSWORD="password"
   XML_FOLDER=/feeds/
   RSS_SCRAPPER_URL=https://rss.example.com/scrapping
   ```

2. Build the container
    ```bash
    make
    ```

Check the [Makefile] for other build targets

### Visual Code Devcontainer

In Visual Code
1. Checkout this git repository
2. Create an `envfile` (see example above)
3. Click "Connections -> Reopen in container"
4. Launch [getcomics_RSS.py](getcomics_RSS.py) either from the debugger or the terminal
