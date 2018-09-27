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
                        'americanas.com.br', 'zol.com.cn', 'axisbank.co.in',
                        'ytimg.com', 'myworkday.com', 'ecosia.org', 'japanpost.jp',
                        'apkpure.com', 'subject.tmall.com', 'kissasian.sh',
                        'ticketmaster.com', 'tencent.com', 'united.com', 'doorblog.jp',
                        'uniqlo.tmall.com', 'toolnewsupdate.info', 'secureserver.net',
                        'bicentenariobu.com', 'macys.com', 'yournewtab.com',
                        'shein.com', 'media.tumblr.com', 'caixa.gov.br', 'uod2quk646.com',
                        'hh.ru', 'nhk.or.jp', 'premium-offers.space', 'crabsecret.tmall.com',
                        'expedia.com', 'browsergames2018.com', 'banesconline.com',
                        'crtmatix.com', 'gstatic.com', 'naukri.com', 'beeg.com',
                        'nike.com', 'chegg.com', 'iitm.ac.in', 'torrentz2.eu',
                        'cbssports.com', 'adp.com', 'torrent9.ph', 'wixsite.com',
                        'slots777.shop', 'mercantilbanco.com', 'alicdn.com', '104.com.tw',
                        'digitaldsp.com', 'namu.wiki', 'subscene.com', 'exhentai.org',
                        'myanimevideo.club', 'accuweather.com', 'kissanime.ru',
                        'jf71qh5v14.com', 'qihoo.com', 'thewhizmarketing.com',
                        'leboncoin.fr', 'gap.tmall.com', 'akamaized.net', 'pixiv.net',
                        'hdfcbank.com', 'sindonews.com', 'bp.blogspot.com',
                        'nextoptim.com', 'cdninstagram.com', 'banvenez.com',
                        'bestbuy.com', 'sjtu.edu.cn', 'retailmenot.com', 'amazon.cn',
                        'hulu.com', 'thepiratebay.org', 'sozcu.com.tr', 'exdynsrv.com',
                        'myshopify.com', 'twimg.com', 'youporn.com', 'ebc.net.tw',
                        'artnewsupdate.info', 'cloudfront.net', 'dailymotion.com',
                        '9amq5z4y1y.com', 'exosrv.com', 'tianya.cn', 'detail.tmall.com',
                        'googleusercontent.com', 'microsoftonline.com', 'pornhub.com',
                        'zomato.com', 'ipleer.fm', 'cbc.ca', 'hootsuite.com', 'un.org',
                        'y8.com', 'socialblade.com', 'thedailybeast.com', 'pirateproxy.gdn',
                        'mufg.jp', 'skysports.com', 'notification-time.com',
                        'shopee.tw', 'thewhizproducts.com', 'tim.it', 'tomshardware.com',
                        'iherb.com', 'nicenewsupdate.info', 'epfindia.gov.in',
                        'cnzz.com', 'v2ex.com']
            with ZipFile(BytesIO(html)) as zf:
                csv_filename = zf.namelist()[0]
                for rank, website in csv.reader(StringIO(zf.open(csv_filename).read().decode())):
                    if website not in bad_urls:
                        urls.append('http://' + website)
                    if len(urls) == self.max_urls:
                        break
        return urls
