import pickle
import os
import re
import urllib.parse
import zlib
from link_crawler import link_crawler


class DiskCache:
    def __init__(self, cache_dir='cache'):
        self.cache_dir = cache_dir

    def __getitem__(self, url):
        """Load data from disk for this URL
        """
        path = self.url_to_path(url)
        if os.path.exists(path):
            with open(path, 'rb') as fp:
                return pickle.loads(zlib.decompress(fp.read()))
        else:
            # URL has not yet been cached
            raise KeyError(url + ' does not exist')

    def __setitem__(self, url, result):
        """Save data to disk for this url
        """
        path = self.url_to_path(url)
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(path, 'wb') as fp:
            fp.write(zlib.compress(pickle.dumps(result)))

    def url_to_path(self, url):
        """Create file system path for this URL
        """
        components = urllib.parse.urlsplit(url)
        # append index.html to empty paths
        path = components.path
        if not path:
            path = '/index.html'
        elif path.endswith('/'):
            path += 'index.html'
        elif path.endswith('index'):
            path += '.html'
        filename = components.netloc + path + components.query
        # replace invalid characters
        filename = re.sub('[^/0-9a-zA-Z\-.,; _]', '_', filename)
        # restric maximum number of characters
        filename = '/'.join(segment[:255] for segment in filename.split('/'))
        return os.path.join(self.cache_dir, filename)


if __name__ == '__main__':
    link_crawler('http://example.webscraping.com',
                 '/places/default/(index|view)', cache=DiskCache())
