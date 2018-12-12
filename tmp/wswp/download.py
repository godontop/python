# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
import urllib.error


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


url= 'https://twitter.com'
ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
proxy = '127.0.0.1:1080'  # Windows上的shadowsocks

download(url, ua, proxy, 2)
