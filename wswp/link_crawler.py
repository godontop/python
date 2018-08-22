# coding=utf-8
import datetime
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
import sys


user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
rp = urllib.robotparser.RobotFileParser()
rp.set_url('http://example.webscraping.com/robots.txt')
rp.read()
proxy = None


class Throttle:
    """Add a delay between downloads to the same domain
    """

    def __init__(self, delay):
        # amount of delay between downloads for each domain
        self.delay = delay
        # timestamp of when a domain was last accessed
        self.domains = {}

    def wait(self, url):
        domain = urllib.parse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)
        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - \
                (datetime.datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                # domain has been accessed recently
                # so need to sleep
                time.sleep(sleep_secs)
        # update the last accessed time
        self.domains[domain] = datetime.datetime.now()


throttle = Throttle(1)


def download(url, user_agent='wswp', proxy=None, num_retries=2):
    '''Support custom User-Agent, proxy and auto retry
    '''
    print('Downloading:', url)  # url is download function's first arguments
    headers = {'User-agent': user_agent}  # user_agent is the second arguments
    request = urllib.request.Request(url, headers=headers)
    opener = urllib.request.build_opener()
    if proxy:
        proxy_params = {urllib.parse.urlparse(url).scheme: proxy}
        opener.add_handler(urllib.request.ProxyHandler(proxy_params))
    try:
        html = opener.open(request).read().decode()
    except urllib.error.URLError as e:
        print('Download error:', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # retry 5XX HTTP errors
                html = download(url, user_agent, proxy, num_retries - 1)
    return html


def link_crawler(seed_url, link_regex, max_depth=2, scrape_callback=None, cache=None):
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
            throttle.wait(url)
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
