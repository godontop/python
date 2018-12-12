import re
import lxml.html
import time
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup

FIELDS = ('area', 'population', 'iso', 'country', 'capital', 'continent', \
          'tld', 'currency_code', 'currency_name', 'phone', \
          'postal_code_format', 'postal_code_regex', 'languages', 'neighbours')


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


def re_scraper(html):
    results = {}
    for field in FIELDS:
        results[field] = re.search('<tr id="places_{}__row">.*?<td class="w2p_fw">(.*?)</td>'.format(field), html).groups()[0]
    return results


def bs_scraper(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = {}
    for field in FIELDS:
        results[field] = soup.find('table').find('tr', id='places_{}__row'.format(field)).find('td', class_='w2p_fw').text
    return results


def lxml_scraper(html):
    tree = lxml.html.fromstring(html)
    results = {}
    for field in FIELDS:
        results[field] = tree.cssselect('table > tr#places_{}__row > td.w2p_fw'.format(field))[0].text_content()
    return results


NUM_ITERATIONS = 1000  # number of times to test each scraper
html = download('http://example.webscraping.com/places/default/view/United-Kingdom-239')
for name, scraper in [('Regular expressions', re_scraper), ('BeautifulSoup', bs_scraper), ('Lxml', lxml_scraper)]:
    # record start time of scrape
    start = time.time()
    for i in range(NUM_ITERATIONS):
        if scraper == re_scraper:
            re.purge()
        result = scraper(html)
        # check scraped result is as expected
        assert(result['area'] == '244,820 square kilometres')
    # record end time of scrape and output the total
    end = time.time()
    print('%s: %.2f seconds' % (name, end - start))
