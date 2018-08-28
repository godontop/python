import pickle
import zlib
from bson.binary import Binary
from datetime import datetime, timedelta
from pymongo import MongoClient
from link_crawler import link_crawler


class MongoCache:
    def __init__(self, client=None, expires=timedelta(days=30)):
        # if a client object is not passed then try connecting to mongodb at
        # the default localhost port
        self.client = MongoClient(
            'localhost', 27017) if client is None else client
        # create collection to store cached webpages, which is the equivalent
        # of a table in a relational database
        self.db = self.client.cache
        # create index to expire cached webpages
        self.db.webpage.create_index(
            'timestamp', expireAfterSeconds=expires.total_seconds())

    def __getitem__(self, url):
        """Load value at this URL
        """
        record = self.db.webpage.find_one({'_id': url})
        if record:
            return pickle.loads(zlib.decompress(record['result']))
        else:
            raise KeyError(url + ' does not exist')

    def __setitem__(self, url, result):
        """Save value for this URL
        """
        record = {'result': Binary(zlib.compress(
            pickle.dumps(result))), 'timestamp': datetime.utcnow()}
        self.db.webpage.update({'_id': url}, {'$set': record}, upsert=True)


if __name__ == '__main__':
    link_crawler('http://example.webscraping.com',
                 '/places/default/(index|view)', max_depth=-1, cache=MongoCache())
