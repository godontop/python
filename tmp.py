# coding: utf8
from urllib.request import build_opener, Request, ProxyHandler
from urllib.parse import urlparse


url = 'http://'
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.183 Safari/537.36 Vivaldi/1.96.1147.64'
headers = {'User-Agent': User_Agent}
req = Request(url, headers=headers)
protocol = urlparse(url).scheme
server = '127.0.0.1:1080'
proxies = {protocol: server}
opener = build_opener()
opener.add_handler(ProxyHandler(proxies))
page = opener.open(req).read().decode()
print(page)