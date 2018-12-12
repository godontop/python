# coding=utf-8
import datetime
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
import sys
from downloader import Downloader


def link_crawler(seed_url, link_regex, delay=1, max_depth=2, user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36', proxies=None, num_retries=2, scrape_callback=None, cache=None):
    """Crawl from the given seed URL following links matched by link_regex
    """
    crawl_queue = [seed_url]
    # keep track which URL's have seen before
    seen = {seed_url: 0}
    num_urls = 0
    rp = get_robots(seed_url)
    D = Downloader(delay=delay, user_agent=user_agent, proxies=proxies,
                   num_retries=num_retries, cache=cache)
    while crawl_queue:
        url = crawl_queue.pop()
        depth = seen[url]
        # check url passes robots.txt restrictions
        if rp.can_fetch(user_agent, url):
            html = D(url)
            links = []
            if scrape_callback:
                links.extend(scrape_callback(url, html) or [])
        else:
            print('Blocked by robots.txt:', url)
            html = None
            sys.exit()
        # filter for links matching our regular expression
        if depth != max_depth:
            for link in get_links(html):
                # check if link matches expected regex
                if re.match(link_regex, link):
                    # form absolute link
                    link = urllib.parse.urljoin(seed_url, link)
                    # check if have already seen this link
                    if link not in seen:
                        seen[link] = depth + 1
                        crawl_queue.append(link)


def get_robots(url):
    """Initialize robots parser for this domain
    """
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(urllib.parse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp


def get_links(html):
    """Return a list of links from html
    """
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(html)
