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


def crawler(seed_url, delay=1, max_depth=2, user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36', proxies=None, num_retries=2, scrape_callback=None, cache=None):
    """Crawl from the given seed URL following links matched by link_regex
    """
    crawl_queue = [seed_url]
    # keep track which URL's have seen before
    seen = {seed_url: 0}
    num_urls = 0
    rp = get_robots(seed_url)
    D = Downloader(delay=delay, user_agent=user_agent, proxies=proxies,
                   num_retries=num_retries, cache=cache)
    if scrape_callback:
        crawl_queue = scrape_callback('http://s3.amazonaws.com/alexa-static/top-1m.csv.zip', D('http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'))
    while crawl_queue:
        url = crawl_queue.pop()
        # check url passes robots.txt restrictions
        if rp.can_fetch(user_agent, url):
            html = D(url)
        else:
            print('Blocked by robots.txt:', url)
            print(user_agent)
            html = None
            sys.exit()


def get_robots(url):
    """Initialize robots parser for this domain
    """
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(urllib.parse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp
