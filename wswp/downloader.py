import datetime
import urllib.parse
import random
import time


DEFAULT_AGENT = 'wswp'

class Downloader:

    def __init__(self, delay=1, user_agent=DEFAULT_AGENT, proxies=None, num_retries=1, cache=None):
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_retries = num_retries
        self.cache = cache

    def __call__(self, url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                # url is not available in cache
                pass
            else:
                if self.num_retries > 0 and 500 <= result['code'] < 600:
                    # server error so ignore result from cache and re-download
                    result = None
        if result is None:
            # result was not loaded from cache
            # so still need to download
            self.throttle.wait(url)
            proxy = random.choice(self.proxies) if self.proxies else None
            headers = {'User-agent': self.user_agent}
            result = self.download(url, headers, proxy, self.num_retries)
            if self.cache:
                # save result to cache
                self.cache[url] = result
        return result['html']

    def download(self, url, headers, proxy, num_retries):
        '''Support custom User-Agent, proxy and auto retry
        '''
        print('Downloading:', url)  # url is download function's first arguments
        request = urllib.request.Request(url, headers=headers)
        opener = urllib.request.build_opener()
        if proxy:
            proxy_params = {urllib.parse.urlparse(url).scheme: proxy}
            opener.add_handler(urllib.request.ProxyHandler(proxy_params))
        try:
            response = opener.open(request)
            html = response.read().decode()
            code = response.code
        except urllib.error.URLError as e:
            print('Download error:', e.reason)
            html = None
            if num_retries > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    # retry 5XX HTTP errors
                    code = e.code
                    html = self.download(url, headers, proxy, num_retries - 1)
            else:
                code = None
        return {'html': html, 'code': code}


class Throttle:
    """Add a delay between downloads to the same domain
    """

    def __init__(self, delay):
        # amount of delay between downloads for each domain
        self.delay = delay
        # timestamp of when a domain was last accessed
        self.domains = {}

    def wait(self, url):
        """Delay if have accessed this domain recently
        """
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
