from datetime import datetime, timedelta
from pymongo import MongoClient


class MongoCache:
    def __init__(self, client=None, expires=timedelta(days=30)):
        # if a client object is not passed then try connecting to mongodb at
        # the default localhost port
        self.client = MongoClient(
            '211.90.242.65', 23270) if client is None else client
        # create collection to store cached webpages, which is the equivalent
        # of a table in a relational database
        self.db = client.cache
        # create index to expire cached webpages
        self.db.webpage.create_index(
            'timestamp', expireAfterSeconds=expires.total_seconds())

    def __getitem__(self, url):
        """Load value at this URL
        """
        record = self.db.webpage.find_one({'_id': url})
        if record:
            return record['result']
        else:
            raise KeyError(url + ' does not exist')

    def __setitem__(self, url, result):
        """Save value for this URL
        """
        record = {'result': result, 'timestamp': datetime.utcnow()}
        self.db.webpage.update({'_id': url}, {'$set': record}, upsert=True)
