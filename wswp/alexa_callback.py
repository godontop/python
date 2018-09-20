import csv
from io import BytesIO, StringIO
from zipfile import ZipFile


class AlexaCallback:
    def __init__(self, max_urls=1000):
        self.max_urls = max_urls
        self.seed_url = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'

    def __call__(self, url, html):
        if url == self.seed_url:
            urls = []
            bad_urls = ['livedoor.biz', 'vkuseraudio.net',
                        'usnews.com', 'special-promotions.online', 'aaucwbe.com',
                        'americanas.com.br']
            with ZipFile(BytesIO(html)) as zf:
                csv_filename = zf.namelist()[0]
                for rank, website in csv.reader(StringIO(zf.open(csv_filename).read().decode())):
                    if website not in bad_urls:
                        urls.append('http://' + website)
                    if len(urls) == self.max_urls:
                        break
        return urls
