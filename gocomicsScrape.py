#!/usr/bin/env python3

import datetime
from html.parser import HTMLParser
import re
import sys
import time
import urllib.request, urllib.parse, urllib.error
import xml.dom.minidom
import json
from xml.sax.saxutils import escape as xml_escape
from playwright.sync_api import sync_playwright

XHTML_NS = "http://www.w3.org/1999/xhtml"

numberOfDaysToScrap = 7
SLEEP_BETWEEN_COMICS = 10
SLEEP_BETWEEN_RETRIES = 600
MAX_RETRIES = 0


def open_url(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        content = page.content() # This will contain the JS-rendered data
        browser.close()
        return content



def get_homepage_data(strip_id):
    class HomepageParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.title = ""
            self.in_title = False

        def handle_starttag(self, tag, attrs):
            if tag == "title":
                self.in_title = True

        def handle_endtag(self, tag):
            if tag == "title":
                self.in_title = False

        def handle_data(self, data):
            if self.in_title and not self.title:
                self.title += data
                self.title = re.sub(r"\s*\|.*$", "", self.title)
                match_obj = re.match("Read (.*) by .*", self.title)
                if match_obj:
                    self.title = match_obj.group(1)

    homepage_url = "https://www.gocomics.com/%s" % strip_id
    homepage_file = open_url(homepage_url)
    parser = HomepageParser()
    parser.feed(homepage_file)
    parser.close()

    if not parser.title:
        return None, []

    today = datetime.date.today()
    strips = []
    for i in range(0, numberOfDaysToScrap):
        strip_date = today - datetime.timedelta(days=i)
        strip_url = "%s/%s" % (homepage_url, strip_date.strftime("%Y/%m/%d"))
        strips.append((strip_date, strip_url))

    return parser.title, strips


def get_strip_image_url(strip_url):
    class ImageParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.image_url = None
            self.in_script = False
            self.in_viewer = False

        def handle_starttag(self, tag, attrs):
            if tag.lower() == "section":
                for attr in attrs:
                    if attr[0] == "class" and "ShowComicViewer" in attr[1]:
                        self.in_viewer = True
            if self.in_viewer and tag.lower() == "script":
                for attr in attrs:
                    if attr[0] == "type" and attr[1] == "application/ld+json":
                        self.in_script = True

        def handle_endtag(self, tag):
            if tag.lower() == "script":
                self.in_script = False
            if tag.lower() == "section":
                self.in_viewer = False

        def handle_data(self, data):
            if self.in_script:
                data = data.encode("utf-8").decode("unicode_escape")
                data = json.loads(data)
                if "@type" in data.keys() and data["@type"] == "ImageObject":
                    #print(data)
                    self.image_url = data["url"]

    parser = ImageParser()
    try:
        strip_file = open_url(strip_url)
    except urllib.error.HTTPError as e:
        if e.code == 302 or e.code == 404:
            # Skip over strip URLs that generate redirects, they must not have
            # existed.
            return None
        else:
            raise
    parser.feed(strip_file)
    parser.close()

    return parser.image_url


def scrape(comic_id):

    title, strips = get_homepage_data(comic_id)

    xmlContent = []
    xmlContent.append('<?xml version="1.0" encoding="utf-8"?>')
    xmlContent.append('<feed xmlns="http://www.w3.org/2005/Atom">')
    xmlContent.append("<title>%s</title>" % xml_escape(title))

    strip_count = 0
    for strip_date, strip_url in strips:
        counter = 0
        # print time.localtime()
        strip_image_url = None
        while True:
            try:
                strip_image_url = get_strip_image_url(strip_url)
                break
            except:
                print(
                    "Retrying %s in %d" % (strip_url, SLEEP_BETWEEN_RETRIES),
                    file=sys.stderr,
                )
                counter = counter + 1
                if counter >= MAX_RETRIES:
                    break
                time.sleep(SLEEP_BETWEEN_RETRIES)
        if not strip_image_url:
            continue
        strip_count += 1
        print('     ',strip_date.isoformat())
        xmlContent.append("<entry>")
        xmlContent.append(
            "  <title>%s</title>" % xml_escape(strip_date.strftime("%A, %B %d, %Y"))
        )
        xmlContent.append("  <id>%s</id>" % strip_url)
        xmlContent.append(
            "  <published>%sT12:00:00.000Z</published>" % strip_date.isoformat()
        )
        xmlContent.append(
            '  <link rel="alternate" href="%s" type="text/html"/>'
            % xml_escape(strip_url)
        )
        xmlContent.append('  <content type="xhtml">')
        xmlContent.append(
            '    <div xmlns="%s"><img src="%s"/></div>'
            % (XHTML_NS, xml_escape(strip_image_url))
        )
        xmlContent.append("  </content>")
        xmlContent.append("</entry>")

        time.sleep(SLEEP_BETWEEN_COMICS)

    # if not strip_count:
    # xmlContent.append '<entry>'
    # xmlContent.append '  <title>Could not scrape feed</title>'
    # xmlContent.append '  <id>tag:persistent.info,2013:gocomics-scrape-%d</id>' % int(time.time())
    # xmlContent.append '  <link rel="alternate" href="https://github.com/mihaip/feed-scraping" type="text/html"/>'
    # xmlContent.append '  <content type="html">'
    # xmlContent.append '    Could not scrape the feed. Check the GitHub repository for updates.'
    # xmlContent.append '  </content>'
    # xmlContent.append '</entry>'

    xmlContent.append("</feed>")

    return "\n".join(xmlContent)
