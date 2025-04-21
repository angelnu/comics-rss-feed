#!/usr/bin/env python3

# importing libraries
from html.parser import HTMLParser
import urllib.request, urllib.error, urllib.parse
import gocomicsScrape
import re
import os
import time
import shutil
import sys
import traceback
import mimetypes
import calendar
import subprocess
import os.path

import requests
import json


print("Starting to scrap!")

#################################
# Variables that need to be set #
#################################
# Tiny Tiny RSS
RSS_URL = os.environ["RSS_URL"]
RSS_LOGIN = os.environ["RSS_LOGIN"]
RSS_PASSWORD = os.environ["RSS_PASSWORD"]


# Directory to stored the generated feeds
XML_FOLDER = os.getenv("XML_FOLDER")
# Where the generated feeds will be served -> must be reachable by the RSS server
RSS_SCRAPPER_URL = os.getenv("RSS_SCRAPPER_URL")

#################################
#    VARIABLES WITH DEFAULTS    #
#################################

# New feeds get added to this category
COMICS_DEFAULT_FEED_CATEGORY_TITLE = os.getenv(
    "COMICS_DEFAULT_FEED_CATEGORY_TITLE", "GoComics"
)
# Favorite feeds category
COMICS_FAVORITE_FEED_CATEGORY_TITLE = os.getenv(
    "COMICS_FAVORITE_FEED_CATEGORY_TITLE", "GoComics-always"
)
# Ignore feeds in this category
COMICS_IGNORE_FEED_CATEGORY_TITLE = os.getenv(
    "COMICS_IGNORE_FEED_CATEGORY_TITLE", "GoComics-ignore"
)


VERBOSE = os.getenv("VERBOSE", False)
MAX_RETRIES = os.getenv("MAX_RETRIES", 10)
RETRIES_WAIT = os.getenv("RETRIES_WAIT", 5)  # In seconds

# Go Comics pages to scrap
URLS_TO_SCRAP = ["https://www.gocomics.com/comics/a-to-z"]
USER_AGENT = os.getenv(
    "USER_AGENT",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
)


def json_rest_post(input_d):
    data_json = json.dumps(input_d, indent=4, sort_keys=True)
    if VERBOSE:
        print("Calling:")
        print(data_json)
    response = requests.post(RSS_URL, data=data_json)
    # print response.text
    result = json.loads(response.text)
    if VERBOSE:
        print((json.dumps(result, indent=4, sort_keys=True)))
    return result


if not os.path.isdir(XML_FOLDER):
    os.mkdir(XML_FOLDER)

# Log into RSS
session_id = json_rest_post(
    {"op": "login", "user": RSS_LOGIN, "password": RSS_PASSWORD}
)["content"]["session_id"]
rss_categories = json_rest_post({"sid": session_id, "op": "getCategories"})["content"]


# Fetch feeds for categories
def get_feeds_for_category(category_title):
    comics_category = [x for x in rss_categories if x["title"] == category_title][0]
    comics_category_id = int(comics_category["id"])
    return (
        comics_category_id,
        json_rest_post(
            {"sid": session_id, "op": "getFeeds", "cat_id": comics_category_id}
        )["content"],
    )


comics_default_feeds_id, comics_default_feeds = get_feeds_for_category(
    COMICS_DEFAULT_FEED_CATEGORY_TITLE
)
comics_favorite_feeds_id, comics_favorite_feeds = get_feeds_for_category(
    COMICS_FAVORITE_FEED_CATEGORY_TITLE
)
comics_ignore_feeds_id, comics_ignore_feeds = get_feeds_for_category(
    COMICS_IGNORE_FEED_CATEGORY_TITLE
)

# Create dictionary of urls
comics_by_url = {}


def add_urls(feeds, is_ignored=False):
    for feed in feeds:
        feed_url = feed["feed_url"]
        comics_by_url[feed_url] = is_ignored


add_urls(comics_default_feeds)
add_urls(comics_favorite_feeds)
add_urls(comics_ignore_feeds, is_ignored=True)


# Parse page
class HomepageParser(HTMLParser):
    def __init__(self, url):
        HTMLParser.__init__(self)
        self.in_script = False
        # Open URL
        req = urllib.request.Request(url)
        req.add_header("User-Agent", USER_AGENT)
        urlopener = urllib.request.urlopen(req)

        # Parse URL
        self.__comic_ids = []
        self.feed(str(urlopener.read()))

        # Close parser and URL
        self.close()
        urlopener.close()

        # Check that we found links
        if len(self.get_comic_ids()) == 0:
            raise NameError("No links found")

    def get_comic_ids(self):
        return self.__comic_ids

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "script":

            for attr in attrs:

                if attr[0] == "type" and attr[1] == "application/ld+json":
                    self.in_script = True
            #         href = attr[1]
            #         # Search for comid_id + date. Example: /the-comic-strip-that-has-a-finale-every-day/2019/12/25
            #         matchObj = re.match("/(.+?) */\d+/\d+/\d+", href)
            #         if matchObj:
            #             comic_id = matchObj.group(1)
            #             self.__comic_ids.append(comic_id)

    def handle_endtag(self, tag):
        if tag.lower() == "script":
            self.in_script = False

    def handle_data(self, data):
        if self.in_script:
            data = data.encode("utf-8").decode("unicode_escape")
            data = json.loads(data)
            if "@type" in data.keys() and data["@type"] == "ItemList":
                print(data)
                for item in data["itemListElement"]:
                    url = item["url"]  # example: 'https://www.gocomics.com/1-and-done'
                    matchObj = re.match(
                        "https://www.gocomics.com/(.*)", url
                    )  # extract the comic id
                    if matchObj:
                        comic_id = matchObj.group(1)
                        self.__comic_ids.append(comic_id)


for url_to_scrap in URLS_TO_SCRAP:

    comic_ids = None
    for retry in range(MAX_RETRIES):
        try:
            parser = HomepageParser(url_to_scrap)
            comic_ids = parser.get_comic_ids()
            break
        except NameError as e:
            print(e)
        except:
            print(("Unknown problem: " + str(url_to_scrap)))
            print((sys.exc_info()[0]), flush=True)

        print("Retry in %s seconds" % (RETRIES_WAIT))
        time.sleep(RETRIES_WAIT)

    if comic_ids == None:
        raise NameError("No more retries for %s" % (url_to_scrap))

    for comic_id in comic_ids:
        print("")
        feed_path = comic_id + ".xml"
        feed_file = XML_FOLDER + feed_path
        feed_url = RSS_SCRAPPER_URL + "/" + feed_path

        if feed_url in comics_by_url:
            # Already known comic
            print("* %s found!" % (comic_id))
            if comics_by_url[feed_url]:
                # Ignored
                print("  - continue (ignore)", flush=True)
                continue
        else:
            # Adding new comic
            print(("Adding " + comic_id), flush=True)
            json_rest_post(
                {
                    "sid": session_id,
                    "op": "subscribeToFeed",
                    "category_id": comics_default_feeds_id,
                    "feed_url": feed_url,
                }
            )

        print(("  - updating feed"), flush=True)
        xmlContent = gocomicsScrape.scrape(comic_id)
        with open(feed_file, "w") as xmlfile:
            xmlfile.write(xmlContent)
