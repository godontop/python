import time
import threading
import urllib.parse
from downloader import Downloader


SLEEP_TIME = 1
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'


def threaded_crawler(seed_url, delay=5, cache=None, scrape_callback=None,
                     user_agent=USER_AGENT, proxies=None, num_retries=1,
                     max_threads=10, timeout=60):
    """Crawl this website in multiple threads
    """
    # the queue of URLs that still need to be crawled
    crawl_queue = [seed_url]
    # the URLs that have been seen
    seen = set([seed_url])
    D = Downloader(cache=cache, delay=delay, user_agent=user_agent,
                   proxies=proxies, num_retries=num_retries, timeout=timeout)

    def process_queue():
        while True:
            try:
                url = crawl_queue.pop()
            except IndexError:
                # crawl queue is empty
                break
            else:
                html = D(url)
                if scrape_callback:
                    try:
                        links = scrape_callback(url, html) or []
                    except Exception as e:
                        print('Error in callback for: {}: {}'.format(url, e))
                    else:
                        for link in links:
                            link = normalize(seed_url, link)
                            # check whether already crawled this link
                            if link not in seen:
                                seen.add(link)
                                # add this new link to queue
                                crawl_queue.append(link)

    # wait for all download threads to finish
    threads = []
    while threads or crawl_quene:
        # the crawl is still active
        for thread in threads:
            if not thread.is_alive():
                # remove the stopped threads
                threads.remove(thread)
        while len(threads) < max_threads and crawl_quene:
            # can start some more threads
            thread = threading.Thread(target=process_queue)
            # set daemon so main thread can exit when receives ctrl-c
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)
        # all threads have been processed
        # sleep temporarily so CPU can focus execution on other threads
        time.sleep(SLEEP_TIME)


def normalize(seed_url, link):
    """Normalize this URL by removing hash and adding domain
    """
    link, _ = urlib.parse.urldefrag(link)  # remove hash to avoid duplicates
    return urlib.parse.urljoin(seed_url, link)
