# -*- coding: utf-8 -*-

from crawler import crawler
from mongo_cache import MongoCache
from alexa_callback import AlexaCallback


def main():
	scrape_callback = AlexaCallback()
	cache = MongoCache()
	# cache.clear()
	crawler(scrape_callback.seed_url, proxies=['127.0.0.1:8118',], scrape_callback=scrape_callback, cache=cache)


if __name__ == '__main__':
	main()